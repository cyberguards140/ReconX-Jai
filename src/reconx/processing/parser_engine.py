import logging


class ParserEngine:
    def __init__(self):
        self.parsers = {}

    def register_parser(self, tool, parser_cls):
        self.parsers[tool] = parser_cls()

    def parse(self, tool, raw_output):
        parser = self.parsers.get(tool)
        if parser:
            try:
                return parser.extract(raw_output)
            except Exception as e:
                logging.error(f"Parser error for {tool}: {e}")
        return []
