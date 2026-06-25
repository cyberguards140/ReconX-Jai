import logging
import re
from typing import Any

logger = logging.getLogger(__name__)


class SearchQueryParser:
    """
    Phase 55: Advanced Search Engine.
    Parses "Google-like" syntax (e.g. `asset:domain severity:critical`)
    into structured database filters.
    """

    def __init__(self):
        pass

    def parse(self, raw_query: str) -> dict[str, Any]:
        """
        Parses a string like 'asset:ip technology:nginx' into a filter dictionary.
        """
        filters = {}

        # Regex to match key:value pairs (handling optional quotes for values)
        pattern = r'([a-zA-Z0-9_]+):(?:([^\s"]+)|"([^"]*)")'

        matches = re.finditer(pattern, raw_query)
        for match in matches:
            key = match.group(1)
            value = match.group(2) if match.group(2) else match.group(3)

            # Group multiple values for the same key into a list
            if key in filters:
                if isinstance(filters[key], list):
                    filters[key].append(value)
                else:
                    filters[key] = [filters[key], value]
            else:
                filters[key] = value

        # Whatever is left over without a 'key:' prefix is treated as a general text search
        text_search = re.sub(pattern, "", raw_query).strip()
        if text_search:
            filters["_text"] = text_search

        logger.debug(f"[Search Engine] Parsed '{raw_query}' into -> {filters}")
        return filters


query_parser = SearchQueryParser()
