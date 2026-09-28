"""
Abiturend MCP server.

Ikkita transport usuli qo'llab-quvvatlanadi:
  * stdio          — lokal (management command `mcp_server`)
  * streamable-http — remote (Stitch-style, docker-compose'dagi `mcp` xizmati)

Ishga tushirish:  python -m mcpbridge.server

Xavfsizlik: HTTP transport `MCP_API_KEY` bearer token'siz so'rovlarni RAD qiladi
(mcpbridge/auth.py). To'g'ri javoblarni ochadigan `include_answers` esa alohida
`MCP_ADMIN_API_KEY` talab qiladi. stdio transport lokal ishonchli jarayon
bo'lgani uchun to'liq huquqlar bilan ishlaydi.
"""

from __future__ import annotations

import os
from typing import Optional

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from mcp.server.fastmcp import FastMCP

from mcpbridge import tools
from mcpbridge.auth import TIER_ADMIN, BearerAuthMiddleware, check_config, set_tier

DEFAULT_PORT = 8001
DEFAULT_PATH = "/mcp/"

mcp = FastMCP(name="abiturend", instructions="Abiturend — DTM/abituriyent platforma ma'lumotlariga MCP orqali kirish.")


@mcp.tool()
def platform_summary() -> dict:
    """Platforma bo'yicha umumiy statistika (fanlar, universitetlar, yo'nalishlar, e'lon qilingan savollar soni)."""
    return tools.platform_summary()


@mcp.tool()
def list_subjects(include_topics: bool = False) -> list[dict]:
    """Barcha faol fanlarni qaytaradi. include_topics=True bo'lsa har bir fanga mavzu/vozmoqchalar qo'shiladi."""
    return tools.search_subjects(include_topics=include_topics)


@mcp.tool()
def get_subject(slug: str, include_topics: bool = True) -> Optional[dict]:
    """Bitta fanni slug bo'yicha qaytaradi. Topilmadi — null."""
    return tools.get_subject(slug, include_topics=include_topics)


@mcp.tool()
def list_universities(city: Optional[str] = None, limit: int = 50) -> list[dict]:
    """Universitetlar ro'yxatini qaytaradi; city bo'yicha filtrlash mumkin."""
    return tools.search_universities(city=city, limit=limit)


@mcp.tool()
def get_university(slug: str, include_directions: bool = True) -> Optional[dict]:
    """Bitta universitetni slug bo'yicha qaytaradi; include_directions=True bo'lsa yo'nalishlari bilan."""
    return tools.get_university(slug, include_directions=include_directions)


@mcp.tool()
def list_directions(
    subject_slug: Optional[str] = None,
    university_slug: Optional[str] = None,
    limit: int = 100,
) -> list[dict]:
    """Yo'nalishlarni qaytaradi; fan (subject_slug) va/yoki universitet (university_slug) bo'yicha filtrlash mumkin."""
    return tools.search_directions(
        subject_slug=subject_slug,
        university_slug=university_slug,
        limit=limit,
    )


@mcp.tool()
def search_questions(
    subject_slug: Optional[str] = None,
    topic_slug: Optional[str] = None,
    difficulty: Optional[int] = None,
    include_answers: bool = False,
    limit: int = 20,
) -> list[dict]:
    """
    E'lon qilingan test savollarini qidiradi (javoblar YASHIRILGAN).

    include_answers=True o'qituvchi/admin uchun to'g'ri javob va izohni ochadi.
    """
    return tools.search_questions(
        subject_slug=subject_slug,
        topic_slug=topic_slug,
        difficulty=difficulty,
        include_answers=include_answers,
        limit=limit,
    )


@mcp.tool()
def get_question(question_id: int, include_answers: bool = False) -> Optional[dict]:
    """Bitta savolni id bo'yicha qaytaradi. include_answers=True bo'lsa to'g'ri javob/izoh ochiladi."""
    return tools.get_question(question_id, include_answers=include_answers)


def build_app(path: str = DEFAULT_PATH):
    """Build the Streamable HTTP ASGI app wrapped in bearer-token auth."""
    check_config()
    app = mcp.streamable_http_app()
    # Well-known liveness path stays open so container/orchestrator probes work.
    return BearerAuthMiddleware(app, exempt_paths={"/healthz", path.rstrip("/") + "/healthz"})


def _run(
    transport: str = "streamable-http",
    host: str = "0.0.0.0",
    port: int = DEFAULT_PORT,
    path: str = DEFAULT_PATH,
) -> None:
    if transport == "stdio":
        # A local, single-user process: run with full tool privileges.
        set_tier(TIER_ADMIN)
        mcp.run(transport="stdio")
        return

    import uvicorn

    set_tier(TIER_ADMIN)
    mcp.settings.host = host
    mcp.settings.port = port
    uvicorn.run(build_app(path), host=host, port=port, log_level="info")


if __name__ == "__main__":
    _run()