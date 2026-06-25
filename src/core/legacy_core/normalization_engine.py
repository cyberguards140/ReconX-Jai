from core.legacy_core.correlation_engine import CorrelationEngine

class NormalizationEngine:
    @staticmethod
    def normalize_and_correlate(parsed_data, project_id, target, source):
        if not parsed_data:
            return
            
        # Standardize missing root values
        if parsed_data.get("value") == "auto" and target:
            # If a tool (like nmap) parses a port but doesn't output the IP on the same line,
            # we default the root value to the original target.
            parsed_data["value"] = target
            parsed_data["type"] = "domain" if "." in target else "ip" # naive check
            
        CorrelationEngine.process_normalized_asset(parsed_data, project_id, source)
