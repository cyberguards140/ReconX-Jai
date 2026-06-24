import csv
import json
import io
from typing import List, Dict, Any, Generator

class DataExporter:
    @staticmethod
    def export_json(data: List[Dict[str, Any]]) -> str:
        """Export data as a JSON string."""
        return json.dumps(data, indent=2, default=str)

    @staticmethod
    def export_csv(data: List[Dict[str, Any]], fieldnames: List[str] = None) -> str:
        """Export data as a CSV string."""
        if not data:
            return ""
        
        if not fieldnames:
            fieldnames = list(data[0].keys())

        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        for row in data:
            writer.writerow(row)
            
        return output.getvalue()

    @staticmethod
    def stream_csv(data_generator: Generator[Dict[str, Any], None, None], fieldnames: List[str]) -> Generator[str, None, None]:
        """Stream data as CSV rows."""
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        yield output.getvalue()
        output.seek(0)
        output.truncate(0)
        
        for row in data_generator:
            writer.writerow(row)
            yield output.getvalue()
            output.seek(0)
            output.truncate(0)
