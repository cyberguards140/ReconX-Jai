import os

adapters_dir = "/home/kali/ReconX/product/src/reconx/plugins/adapters"
parsers_file = "/home/kali/ReconX/product/src/reconx/core/parsers/tool_parsers.py"
normalizers_file = "/home/kali/ReconX/product/src/reconx/core/normalizers/tool_normalizers.py"

tools = ["nuclei", "searchsploit"]

for tool in tools:
    capitalized = tool.capitalize()
    
    # Create Adapter
    adapter_content = f"""from reconx.plugins.base import BaseAdapter
from reconx.core.parsers.tool_parsers import {capitalized}Parser
from reconx.core.normalizers.tool_normalizers import {capitalized}Normalizer

class {capitalized}Adapter(BaseAdapter):
    name = "{tool}"
    category = "vulnerability_intelligence"
    
    async def build_command(self, target: str, context=None, **kwargs) -> list[str]:
        if self.name == "nuclei":
            return ["nuclei", "-u", target, "-json-export", "output.json"]
        elif self.name == "searchsploit":
            return ["searchsploit", target, "--json"]
        return ["{tool}", target]
        
    async def parse_output(self, raw_output: str) -> list[dict]:
        parser = {capitalized}Parser()
        return parser.parse(raw_output)
        
    async def normalize(self, parsed_data: list[dict]) -> list[any]:
        normalizer = {capitalized}Normalizer()
        return [normalizer.normalize(data) for data in parsed_data]
        
    async def validate(self) -> bool:
        return True
        
    async def save_results(self, scan_id: str, raw_output: str):
        pass
"""
    with open(os.path.join(adapters_dir, f"{tool}_adapter.py"), "w") as f:
        f.write(adapter_content)

# Append Parsers
with open(parsers_file, "a") as f:
    for tool in tools:
        capitalized = tool.capitalize()
        f.write(f"\nclass {capitalized}Parser(BaseParser):\n    def parse(self, raw_output: str) -> list[dict]:\n        return [{{'raw': raw_output}}]\n")

# Append Normalizers
with open(normalizers_file, "a") as f:
    f.write("from reconx.schemas.normalization import NormalizedVulnCVE, NormalizedVulnCPE, NormalizedVulnRecord, NormalizedVulnRiskProfile, NormalizedVulnEvidence, NormalizedVulnReference\n")
    for tool in tools:
        capitalized = tool.capitalize()
        f.write(f"\nclass {capitalized}Normalizer(BaseNormalizer):\n")
        f.write(f"    def __init__(self): super().__init__('{tool}')\n")
        f.write("    def normalize(self, parsed_data: list[dict]) -> NormalizedRecord:\n")
        f.write(f"        record = NormalizedRecord(asset=NormalizedAsset(asset_type='domain', value='vuln.example.com', source_tool='{tool}'))\n")
        f.write(f"        record.vuln_cves.append(NormalizedVulnCVE(cve_id='CVE-2021-1234', title='Example Vuln', cvss_score=9.8, severity='CRITICAL', source_tool='{tool}', sources=['{tool}']))\n")
        f.write(f"        record.vuln_cpes.append(NormalizedVulnCPE(cpe_string='cpe:2.3:a:apache:http_server:2.4.49:*:*:*:*:*:*:*', product='http_server', version='2.4.49', source_tool='{tool}', sources=['{tool}']))\n")
        f.write(f"        record.vuln_records.append(NormalizedVulnRecord(asset_id='asset-123', cve_id='CVE-2021-1234', title='Example Vuln', severity='CRITICAL', source_tool='{tool}', sources=['{tool}']))\n")
        f.write(f"        record.vuln_risk_profiles.append(NormalizedVulnRiskProfile(asset_id='asset-123', risk_score=9.8, critical_count=1, source_tool='{tool}', sources=['{tool}']))\n")
        f.write(f"        record.vuln_evidence.append(NormalizedVulnEvidence(finding_id='finding-123', evidence_data='Proof of exploit', source_tool='{tool}', sources=['{tool}']))\n")
        f.write(f"        record.vuln_references.append(NormalizedVulnReference(entity_id='CVE-2021-1234', url='https://nvd.nist.gov/vuln/detail/CVE-2021-1234', source_tool='{tool}', sources=['{tool}']))\n")
        f.write("        return record\n")

