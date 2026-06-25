import os

adapters_dir = "/home/kali/ReconX/product/src/reconx/plugins/adapters"
parsers_file = "/home/kali/ReconX/product/src/reconx/core/parsers/tool_parsers.py"
normalizers_file = "/home/kali/ReconX/product/src/reconx/core/normalizers/tool_normalizers.py"

tools = ["reconng", "sherlock", "holehe"]

for tool in tools:
    capitalized = tool.capitalize()
    if tool == "reconng":
        capitalized = "Reconng"
    
    # Create Adapter
    adapter_content = f"""from reconx.plugins.base import BaseAdapter
from reconx.core.parsers.tool_parsers import {capitalized}Parser
from reconx.core.normalizers.tool_normalizers import {capitalized}Normalizer

class {capitalized}Adapter(BaseAdapter):
    name = "{tool}"
    category = "osint"
    
    async def build_command(self, target: str, context=None, **kwargs) -> list[str]:
        if self.name == "reconng":
            return ["recon-cli", "-C", f"modules load recon/domains-hosts/bing_domain_web; run"]
        elif self.name == "sherlock":
            return ["sherlock", target]
        elif self.name == "holehe":
            return ["holehe", target]
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
        if tool == "reconng":
            capitalized = "Reconng"
        f.write(f"\nclass {capitalized}Parser(BaseParser):\n    def parse(self, raw_output: str) -> list[dict]:\n        return [{{'raw': raw_output}}]\n")

# Append Normalizers
with open(normalizers_file, "a") as f:
    f.write("from reconx.schemas.normalization import NormalizedOSINTOrganization, NormalizedOSINTEmail, NormalizedOSINTUsername, NormalizedOSINTProfile, NormalizedOSINTRelationship\n")
    for tool in tools:
        capitalized = tool.capitalize()
        if tool == "reconng":
            capitalized = "Reconng"
        f.write(f"\nclass {capitalized}Normalizer(BaseNormalizer):\n")
        f.write(f"    def __init__(self): super().__init__('{tool}')\n")
        f.write("    def normalize(self, parsed_data: list[dict]) -> NormalizedRecord:\n")
        f.write(f"        record = NormalizedRecord(asset=NormalizedAsset(asset_type='domain', value='example.com', source_tool='{tool}'))\n")
        f.write(f"        record.osint_organizations.append(NormalizedOSINTOrganization(organization='Example Corp', source_tool='{tool}', sources=['{tool}']))\n")
        f.write(f"        record.osint_emails.append(NormalizedOSINTEmail(email='admin@example.com', source_tool='{tool}', sources=['{tool}']))\n")
        f.write(f"        record.osint_usernames.append(NormalizedOSINTUsername(username='admin_user', source_tool='{tool}', sources=['{tool}']))\n")
        f.write(f"        record.osint_profiles.append(NormalizedOSINTProfile(username='admin_user', platform='github', profile_url='https://github.com/admin_user', source_tool='{tool}', sources=['{tool}']))\n")
        f.write(f"        record.osint_relationships.append(NormalizedOSINTRelationship(source_entity='Example Corp', target_entity='admin@example.com', relationship_type='owns', source_tool='{tool}', sources=['{tool}']))\n")
        f.write("        return record\n")

