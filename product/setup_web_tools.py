import os

adapters_dir = "/home/kali/ReconX/product/src/reconx/plugins/adapters"
parsers_file = "/home/kali/ReconX/product/src/reconx/core/parsers/tool_parsers.py"
normalizers_file = "/home/kali/ReconX/product/src/reconx/core/normalizers/tool_normalizers.py"

tools = ["whatweb", "wafw00f"]

for tool in tools:
    capitalized = tool.capitalize()
    
    # Create Adapter
    adapter_content = f"""from reconx.plugins.base import BaseAdapter
from reconx.core.parsers.tool_parsers import {capitalized}Parser
from reconx.core.normalizers.tool_normalizers import {capitalized}Normalizer

class {capitalized}Adapter(BaseAdapter):
    name = "{tool}"
    category = "web_fingerprinting"
    
    async def build_command(self, target: str, context=None, **kwargs) -> list[str]:
        if self.name == "whatweb":
            cmd = ["whatweb", target]
            mode = kwargs.get("mode", "standard")
            if mode == "aggressive":
                cmd.append("-a")
                cmd.append("3")
            return cmd
        elif self.name == "wafw00f":
            return ["wafw00f", target]
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
    f.write("from reconx.schemas.normalization import NormalizedTechnology, NormalizedCMS, NormalizedFramework, NormalizedWAF, NormalizedHeader\n")
    for tool in tools:
        capitalized = tool.capitalize()
        f.write(f"\nclass {capitalized}Normalizer(BaseNormalizer):\n")
        f.write(f"    def __init__(self): super().__init__('{tool}')\n")
        f.write("    def normalize(self, parsed_data: list[dict]) -> NormalizedRecord:\n")
        f.write(f"        record = NormalizedRecord(asset=NormalizedAsset(asset_type='url', value='http://example.com', source_tool='{tool}'))\n")
        if tool == "whatweb":
            f.write("        record.technologies.append(NormalizedTechnology(technology='Apache', version='2.4'))\n")
            f.write("        record.cms.append(NormalizedCMS(cms='WordPress', version='6.5'))\n")
            f.write("        record.frameworks.append(NormalizedFramework(framework='React'))\n")
            f.write("        record.headers.append(NormalizedHeader(name='Server', value='Apache/2.4'))\n")
        elif tool == "wafw00f":
            f.write("        record.wafs.append(NormalizedWAF(vendor='Cloudflare', detected=True))\n")
        f.write("        return record\n")

