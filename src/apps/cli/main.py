import argparse
import logging

from apps.api_gateway.server import start_server
from core.config.settings import settings
from core.constants.version import __version__
from core.logging.logger import setup_logging

logger = logging.getLogger("reconx")

BANNER = f"""
===================================================
                RECONX v{__version__} FINAL
         Enterprise SaaS / API Backend Service
===================================================
"""


def main():
    print(BANNER)
    setup_logging()

    logger.info("ReconX Configuration Loaded")
    logger.info(f"Project ID: {settings.project_id}")
    logger.info(f"Database: {settings.database_url}")

    parser = argparse.ArgumentParser(description="ReconX API Service")
    parser.add_argument(
        "action",
        choices=["api", "cli"],
        nargs="?",
        default="cli",
        help="Launch the API Server or CLI",
    )
    parser.add_argument("--port", type=int, default=8000, help="Port to bind")

    args = parser.parse_args()

    if args.action == "api":
        start_server(args.port)
    elif args.action == "cli":
        from apps.cli.menu import display_menu
        from apps.dashboard.backend.dashboard_manager import DashboardManager

        class DummySession:
            def __init__(self):
                self.project_id = None
                self.current_project = None

            def set_project(self, name, pid):
                self.current_project = name
                self.project_id = pid

        display_menu(DummySession(), settings, DashboardManager())


if __name__ == "__main__":
    main()
