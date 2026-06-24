import os

adapters_dir = "/home/kali/ReconX/product/src/reconx/plugins/adapters"
parsers_file = "/home/kali/ReconX/product/src/reconx/core/parsers/tool_parsers.py"
normalizers_file = "/home/kali/ReconX/product/src/reconx/core/normalizers/tool_normalizers.py"

tools = ["gobuster", "feroxbuster", "dirb", "dirsearch", "ffuf", "wfuzz"]

for tool in tools:
    capitalized = tool.capitalize()
    
    # Create Adapter
    adapter_content = f"""from reconx.plugins.base import BaseAdapter
from reconx.core.parsers.tool_parsers import {capitalized}Parser
from reconx.core.normalizers.tool_normalizers import {capitalized}Normalizer

class {capitalized}Adapter(BaseAdapter):
    name = "{tool}"
    category = "content_discovery"
    
    async def build_command(self, target: str, context=None, **kwargs) -> list[str]:
        if self.name == "gobuster":
            return ["gobuster", "dir", "-u", target]
        elif self.name == "ffuf":
            return ["ffuf", "-u", target + "/FUZZ"]
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
    f.write("from reconx.schemas.normalization import NormalizedContent, NormalizedEndpoint, NormalizedVirtualHost\n")
    for tool in tools:
        capitalized = tool.capitalize()
        f.write(f"\nclass {capitalized}Normalizer(BaseNormalizer):\n")
        f.write(f"    def __init__(self): super().__init__('{tool}')\n")
        f.write("    def normalize(self, parsed_data: list[dict]) -> NormalizedRecord:\n")
        f.write(f"        record = NormalizedRecord(asset=NormalizedAsset(asset_type='url', value='http://example.com', source_tool='{tool}'))\n")
        f.write(f"        record.contents.append(NormalizedContent(url='http://example.com/admin', path='/admin', status_code=200, source_tool='{tool}', sources=['{tool}']))\n")
        f.write(f"        record.endpoints.append(NormalizedEndpoint(method='GET', path='/api/v1/users', source_tool='{tool}', sources=['{tool}']))\n")
        f.write(f"        record.vhosts.append(NormalizedVirtualHost(vhost='admin.example.com', source_tool='{tool}', sources=['{tool}']))\n")
        f.write("        return record\n")

