"""
MCP transport authentication.

The MCP bridge is exposed over Streamable HTTP through nginx, so it is reachable
from the public internet. The question bank contains official exam answers, so
the bridge must never serve data anonymously:

* every HTTP request must carry ``Authorization: Bearer <MCP_API_KEY>``
* tools that reveal correct answers (``include_answers=True``) additionally
  require ``MCP_ADMIN_API_KEY``

Both checks fail closed: with no configured key the bridge rejects every request
instead of defaulting to open access. The authenticated tier is published through
a :class:`contextvars.ContextVar` so tool functions can gate privileged output
without threading the request object through the MCP SDK.

The local ``stdio`` transport is a trusted single-user process, so it runs with
full (admin) privileges.
"""

from __future__ import annotations

import hmac
import logging
from contextvars import ContextVar

from django.conf import settings

logger = logging.getLogger(__name__)

TIER_ANONYMOUS = "anonymous"
TIER_READ = "read"
TIER_ADMIN = "admin"

_tier: ContextVar[str] = ContextVar("mcp_auth_tier", default=TIER_ANONYMOUS)


class McpAuthError(RuntimeError):
    """Raised when a tool is called without the privileges it requires."""


def current_tier() -> str:
    return _tier.get()


def is_admin() -> bool:
    return _tier.get() == TIER_ADMIN


def set_tier(tier: str):
    """Set the ambient auth tier (used by tests and the stdio transport)."""
    return _tier.set(tier)


def _secret(name: str) -> str:
    return (getattr(settings, name, "") or "").strip()


def api_key() -> str:
    return _secret("MCP_API_KEY")


def admin_api_key() -> str:
    return _secret("MCP_ADMIN_API_KEY")


def is_configured() -> bool:
    """True when at least the read-level key is configured."""
    return bool(api_key())


def check_config() -> None:
    """Raise if the HTTP transport would run without a usable key."""
    if not is_configured():
        raise RuntimeError(
            "MCP_API_KEY is not configured. Set it before starting the MCP HTTP "
            "transport, otherwise /mcp/ would reject every request. Generate one "
            "with: python -c \"import secrets; print(secrets.token_urlsafe(32))\""
        )


def _bearer_token(headers) -> str:
    raw = ""
    for name, value in headers:
        if name.lower() == b"authorization":
            raw = value.decode("latin-1")
            break
    if not raw:
        return ""
    scheme, _, token = raw.partition(" ")
    if scheme.lower() != "bearer":
        return ""
    return token.strip()


def authenticate(token: str) -> str:
    """Map a bearer token to an auth tier. Unknown tokens map to anonymous."""
    read_key = api_key()
    admin_key = admin_api_key()

    if admin_key and token and hmac.compare_digest(token.encode(), admin_key.encode()):
        return TIER_ADMIN
    if read_key and token and hmac.compare_digest(token.encode(), read_key.encode()):
        return TIER_READ
    return TIER_ANONYMOUS


def require_admin(action: str) -> None:
    """Guard privileged tool output."""
    if is_admin():
        return
    raise McpAuthError(
        f"{action} requires an elevated MCP key. Configure MCP_ADMIN_API_KEY and "
        "call the bridge with that bearer token."
    )


async def _unauthorized(send, status: int, detail: str) -> None:
    body = detail.encode("utf-8")
    headers = [
        (b"content-type", b"application/json"),
        (b"content-length", str(len(body)).encode("latin-1")),
        (b"www-authenticate", b"Bearer"),
    ]
    await send({"type": "http.response.start", "status": status, "headers": headers})
    await send({"type": "http.response.body", "body": body})


class BearerAuthMiddleware:
    """Pure-ASGI bearer-token gate for the Streamable HTTP transport.

    Wrapping at the ASGI layer (rather than inside tools) means unauthenticated
    callers cannot even enumerate the tool list.
    """

    def __init__(self, app, exempt_paths=()):
        self.app = app
        self.exempt_paths = set(exempt_paths)

    async def __call__(self, scope, receive, send):
        if scope.get("type") != "http":
            await self.app(scope, receive, send)
            return

        if not is_configured():
            logger.error(
                "MCP_API_KEY is empty - rejecting all MCP requests. Set MCP_API_KEY "
                "in the environment."
            )
            await _unauthorized(
                send,
                503,
                '{"error":"mcp_not_configured","detail":"MCP_API_KEY is not configured."}',
            )
            return

        if scope.get("path") in self.exempt_paths:
            await self.app(scope, receive, send)
            return

        tier = authenticate(_bearer_token(scope.get("headers") or []))
        if tier == TIER_ANONYMOUS:
            logger.warning("MCP request rejected: missing or invalid bearer token")
            await _unauthorized(
                send,
                401,
                '{"error":"unauthorized","detail":"Valid bearer token required."}',
            )
            return

        token = _tier.set(tier)
        try:
            await self.app(scope, receive, send)
        finally:
            _tier.reset(token)
