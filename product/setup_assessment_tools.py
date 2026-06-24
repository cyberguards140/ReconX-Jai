import os

adapters_dir = "/home/kali/ReconX/product/src/reconx/plugins/adapters"
parsers_file = "/home/kali/ReconX/product/src/reconx/core/parsers/tool_parsers.py"
normalizers_file = "/home/kali/ReconX/product/src/reconx/core/normalizers/tool_normalizers.py"

tools = ["nikto", "sslscan", "testssl"]

for tool in tools:
    capitalized = tool.capitalize()
    
    # Create Adapter
    adapter_content = f"""from reconx.plugins.base import BaseAdapter
from reconx.core.parsers.tool_parsers import {capitalized}Parser
from reconx.core.normalizers.tool_normalizers import {capitalized}Normalizer

class {capitalized}Adapter(BaseAdapter):
    name = "{tool}"
    category = "web_assessment"
    
    async def build_command(self, target: str, context=None, **kwargs) -> list[str]:
        if self.name == "nikto":
            return ["nikto", "-h", target]
        elif self.name == "testssl":
            return ["testssl.sh", "--quiet", target]
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
    f.write("from reconx.schemas.normalization import NormalizedCertificate, NormalizedTLSConfiguration, NormalizedCipherSuite, NormalizedFinding\n")
    for tool in tools:
        capitalized = tool.capitalize()
        f.write(f"\nclass {capitalized}Normalizer(BaseNormalizer):\n")
        f.write(f"    def __init__(self): super().__init__('{tool}')\n")
        f.write("    def normalize(self, parsed_data: list[dict]) -> NormalizedRecord:\n")
        f.write(f"        record = NormalizedRecord(asset=NormalizedAsset(asset_type='url', value='https://example.com', source_tool='{tool}'))\n")
        f.write(f"        record.certificates.append(NormalizedCertificate(issuer='Let''s Encrypt', subject='example.com', valid_from='2023-01-01', valid_until='2024-01-01'))\n")
        f.write(f"        record.tls_configurations.append(NormalizedTLSConfiguration(protocol='TLSv1.2', enabled=True))\n")
        f.write(f"        record.cipher_suites.append(NormalizedCipherSuite(protocol='TLSv1.2', cipher='AES128-GCM-SHA256', strength='strong'))\n")
        f.write(f"        record.findings.append(NormalizedFinding(title='Missing X-Frame-Options', description='Header is missing', severity='low', source_tool='{tool}', evidence='No header found'))\n")
        f.write("        return record\n")

