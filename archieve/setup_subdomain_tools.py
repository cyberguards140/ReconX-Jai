import os

adapters_dir = "/home/kali/ReconX/product/src/reconx/plugins/adapters"
parsers_file = "/home/kali/ReconX/product/src/reconx/core/parsers/tool_parsers.py"
normalizers_file = "/home/kali/ReconX/product/src/reconx/core/normalizers/tool_normalizers.py"

tools = ["amass", "theharvester"]

for tool in tools:
    capitalized = tool.capitalize()
    
    # Create Adapter
    adapter_content = f"""from reconx.plugins.base import BaseAdapter
from reconx.core.parsers.tool_parsers import {capitalized}Parser
from reconx.core.normalizers.tool_normalizers import {capitalized}Normalizer

class {capitalized}Adapter(BaseAdapter):
    name = "{tool}"
    category = "subdomains"
    
    async def build_command(self, target: str, context=None, **kwargs) -> list[str]:
        if self.name == "amass":
            mode = kwargs.get("mode", "passive")
            cmd = ["amass", "enum", "-d", target]
            if mode == "passive":
                cmd.append("-passive")
            elif mode == "active":
                cmd.append("-active")
            return cmd
        elif self.name == "theharvester":
            return ["theHarvester", "-d", target, "-b", "all"]
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
    for tool in tools:
        capitalized = tool.capitalize()
        f.write(f"\nclass {capitalized}Normalizer(BaseNormalizer):\n")
        f.write(f"    def __init__(self): super().__init__('{tool}')\n")
        f.write("    def normalize(self, parsed_data: list[dict]) -> NormalizedRecord:\n")
        f.write(f"        record = NormalizedRecord(asset=NormalizedAsset(asset_type='subdomain', value='api.example.com', source_tool='{tool}', sources=['{tool}']))\n")
        f.write("        return record\n")

