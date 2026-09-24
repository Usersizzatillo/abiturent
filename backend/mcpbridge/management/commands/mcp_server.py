"""
Abiturend MCP serverini ishga tushirish.

  python manage.py mcp_server                       # stdio (lokal MCP client)
  python manage.py mcp_server --transport http      # streamable-http (remote)
"""

from django.core.management.base import BaseCommand

from mcpbridge.server import _run, DEFAULT_PATH, DEFAULT_PORT


class Command(BaseCommand):
    help = "Abiturend MCP serverini ishga tushiradi (stdio yoki streamable-http)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--transport",
            default="stdio",
            choices=["stdio", "http"],
            help="Transport: stdio (default) yoki http (streamable-http).",
        )
        parser.add_argument("--host", default="0.0.0.0", help="HTTP transport host.")
        parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="HTTP transport port.")
        parser.add_argument(
            "--path",
            default=DEFAULT_PATH,
            help="HTTP transport path (default: /mcp/).",
        )

    def handle(self, *args, **options):
        if options["transport"] == "http":
            self.stdout.write(
                self.style.SUCCESS(
                    f"MCP streamable-http: http://{options['host']}:{options['port']}{options['path']}"
                )
            )
            _run(
                transport="streamable-http",
                host=options["host"],
                port=options["port"],
                path=options["path"],
            )
        else:
            self.stdout.write(self.style.SUCCESS("MCP stdio server ishga tushdi."))
            _run(transport="stdio")