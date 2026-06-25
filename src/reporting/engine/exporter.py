import csv
import io
import json
from collections.abc import Generator
from typing import Any


class DataExporter:
    @staticmethod
    def export_json(data: list[dict[str, Any]]) -> str:
        """Export data as a JSON string."""
        return json.dumps(data, indent=2, default=str)

    @staticmethod
    def export_csv(data: list[dict[str, Any]], fieldnames: list[str] = None) -> str:
        """Export data as a CSV string."""
        if not data:
            return ""

        if not fieldnames:
            fieldnames = list(data[0].keys())

        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in data:
            writer.writerow(row)

        return output.getvalue()

    @staticmethod
    def stream_csv(
        data_generator: Generator[dict[str, Any], None, None], fieldnames: list[str]
    ) -> Generator[str, None, None]:
        """Stream data as CSV rows."""
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        yield output.getvalue()
        output.seek(0)
        output.truncate(0)

        for row in data_generator:
            writer.writerow(row)
            yield output.getvalue()
            output.seek(0)
            output.truncate(0)
