import logging
import os
from typing import Any

import aiohttp

logger = logging.getLogger(__name__)


class ThreatIntelEngine:
    """
    Enriches assets by querying third-party OSINT APIs (Shodan, VirusTotal).
    """

    def __init__(self):
        self.shodan_key = os.environ.get("SHODAN_API_KEY")
        self.vt_key = os.environ.get("VT_API_KEY")

    async def enrich_asset(self, asset: dict[str, Any]) -> dict[str, Any]:
        """
        Takes a raw asset dictionary and appends threat intelligence data.
        """
        target = asset.get("target")
        if not target:
            return asset

        asset["threat_intel"] = {}

        # Shodan Enrichment
        if self.shodan_key:
            shodan_data = await self._query_shodan(target)
            if shodan_data:
                asset["threat_intel"]["shodan"] = shodan_data
        else:
            logger.debug("Skipping Shodan enrichment: Missing API Key")

        # VirusTotal Enrichment
        if self.vt_key:
            vt_data = await self._query_virustotal(target)
            if vt_data:
                asset["threat_intel"]["virustotal"] = vt_data
        else:
            logger.debug("Skipping VirusTotal enrichment: Missing API Key")

        return asset

    async def _query_shodan(self, target: str) -> dict[str, Any]:
        url = f"https://api.shodan.io/shodan/host/{target}?key={self.shodan_key}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=5) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return {
                            "ports": data.get("ports", []),
                            "tags": data.get("tags", []),
                            "vulns": data.get("vulns", []),
                        }
        except Exception as e:
            logger.warning(f"Shodan query failed for {target}: {e}")
        return {}

    async def _query_virustotal(self, target: str) -> dict[str, Any]:
        # Implementation for VT API v3
        url = f"https://www.virustotal.com/api/v3/domains/{target}"
        headers = {"x-apikey": self.vt_key}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, timeout=5) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        stats = (
                            data.get("data", {})
                            .get("attributes", {})
                            .get("last_analysis_stats", {})
                        )
                        return {
                            "malicious": stats.get("malicious", 0),
                            "suspicious": stats.get("suspicious", 0),
                        }
        except Exception as e:
            logger.warning(f"VirusTotal query failed for {target}: {e}")
        return {}


threat_intel_engine = ThreatIntelEngine()
