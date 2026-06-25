from datetime import datetime
from typing import Any

import jinja2
from weasyprint import HTML


class ReportRenderer:
    def __init__(self, templates_dir: str):
        self.templates_dir = templates_dir
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.templates_dir),
            autoescape=jinja2.select_autoescape(["html", "xml"]),
        )
        # Register custom filters
        self.env.filters["datetime"] = self._format_datetime
        self.env.filters["severity_color"] = self._severity_color

    def _format_datetime(self, value, format="%Y-%m-%d %H:%M:%S"):
        if isinstance(value, str):
            try:
                value = datetime.fromisoformat(value)
            except ValueError:
                return value
        if isinstance(value, datetime):
            return value.strftime(format)
        return value

    def _severity_color(self, severity: str) -> str:
        colors = {
            "critical": "#dc2626",  # Red
            "high": "#ea580c",  # Orange
            "medium": "#eab308",  # Yellow
            "low": "#3b82f6",  # Blue
            "info": "#6b7280",  # Gray
        }
        return colors.get(str(severity).lower(), "#6b7280")

    def render_html(self, template_name: str, context: dict[str, Any]) -> str:
        """Render a Jinja2 template to HTML string."""
        template = self.env.get_template(template_name)
        return template.render(**context)

    def render_pdf(
        self, template_name: str, context: dict[str, Any], output_path: str | None = None
    ) -> bytes:
        """Render a Jinja2 template to PDF and optionally save it to output_path."""
        html_content = self.render_html(template_name, context)
        html = HTML(string=html_content, base_url=self.templates_dir)

        if output_path:
            html.write_pdf(output_path)
            with open(output_path, "rb") as f:
                return f.read()
        else:
            return html.write_pdf()


renderer_instance = None


def get_renderer(templates_dir: str) -> ReportRenderer:
    global renderer_instance
    if not renderer_instance or renderer_instance.templates_dir != templates_dir:
        renderer_instance = ReportRenderer(templates_dir)
    return renderer_instance
