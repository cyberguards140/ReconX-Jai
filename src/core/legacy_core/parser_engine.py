from core.legacy_core.normalization_engine import NormalizationEngine


class ParserEngine:
    parsers = {}

    @classmethod
    def load_parsers(cls):
        # Basic dynamic load (In production, would be more robust)
        try:
            import parsers.dnsx_parser
            import parsers.httpx_parser
            import parsers.nmap_parser
            import parsers.subfinder_parser

            cls.parsers["nmap"] = parsers.nmap_parser
            cls.parsers["subfinder"] = parsers.subfinder_parser
            cls.parsers["dnsx"] = parsers.dnsx_parser
            cls.parsers["httpx"] = parsers.httpx_parser
        except:
            pass

    @classmethod
    def parse(cls, tool_id, project_id, target, line):
        if not cls.parsers:
            cls.load_parsers()

        parser = cls.parsers.get(tool_id)
        if parser and hasattr(parser, "parse"):
            parsed_data = parser.parse(line)
            if parsed_data:
                NormalizationEngine.normalize_and_correlate(
                    parsed_data, project_id, target, tool_id
                )
