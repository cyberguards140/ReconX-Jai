import json
import csv
import io

class ExportEngine:
    """Exports structured dictionaries into various formats."""
    
    @staticmethod
    def export_json(data: dict) -> str:
        return json.dumps(data, indent=2)
        
    @staticmethod
    def export_csv(headers: list, rows: list) -> str:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(headers)
        writer.writerows(rows)
        return output.getvalue()
        
    @staticmethod
    def export_html(title: str, body: str) -> str:
        return f"<html><head><title>{title}</title></head><body>{body}</body></html>"
        
    @staticmethod
    def export_pdf(title: str, body: str) -> bytes:
        # Mocking PDF generation
        return f"PDF_MOCK_CONTENT: {title}\n{body}".encode()
