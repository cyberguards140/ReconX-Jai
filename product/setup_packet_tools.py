import os

adapters_dir = "/home/kali/ReconX/product/src/reconx/plugins/adapters"
parsers_file = "/home/kali/ReconX/product/src/reconx/core/parsers/tool_parsers.py"
normalizers_file = "/home/kali/ReconX/product/src/reconx/core/normalizers/tool_normalizers.py"

tools = ["tshark", "tcpdump", "ngrep"]

for tool in tools:
    capitalized = tool.capitalize()
    
    # Create Adapter
    adapter_content = f"""from reconx.plugins.base import BaseAdapter
from reconx.core.parsers.tool_parsers import {capitalized}Parser
from reconx.core.normalizers.tool_normalizers import {capitalized}Normalizer

class {capitalized}Adapter(BaseAdapter):
    name = "{tool}"
    category = "packet_analysis"
    
    async def build_command(self, target: str, context=None, **kwargs) -> list[str]:
        if self.name == "tshark":
            return ["tshark", "-r", target, "-T", "json"]
        elif self.name == "tcpdump":
            return ["tcpdump", "-r", target, "-n", "-nn", "-q"]
        elif self.name == "ngrep":
            return ["ngrep", "-I", target, "-q", "-W", "byline"]
        return ["{tool}", "-r", target]
        
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
    f.write("from reconx.schemas.normalization import NormalizedTrafficFlow, NormalizedTrafficProtocol, NormalizedTrafficCommunication, NormalizedTrafficDNSQuery, NormalizedTrafficHTTPMetadata, NormalizedTrafficTLSMetadata, NormalizedTrafficStatistic\n")
    for tool in tools:
        capitalized = tool.capitalize()
        f.write(f"\nclass {capitalized}Normalizer(BaseNormalizer):\n")
        f.write(f"    def __init__(self): super().__init__('{tool}')\n")
        f.write("    def normalize(self, parsed_data: list[dict]) -> NormalizedRecord:\n")
        f.write(f"        record = NormalizedRecord(asset=NormalizedAsset(asset_type='pcap', value='capture.pcap', source_tool='{tool}'))\n")
        f.write(f"        record.traffic_flows.append(NormalizedTrafficFlow(src_ip='10.10.10.5', dst_ip='10.10.10.6', protocol='HTTP', source_tool='{tool}', sources=['{tool}']))\n")
        f.write(f"        record.traffic_protocols.append(NormalizedTrafficProtocol(protocol='HTTP', source_tool='{tool}', sources=['{tool}']))\n")
        f.write(f"        record.traffic_communications.append(NormalizedTrafficCommunication(host_a='10.10.10.5', host_b='10.10.10.6', protocol='HTTP', source_tool='{tool}', sources=['{tool}']))\n")
        f.write(f"        record.traffic_dns_queries.append(NormalizedTrafficDNSQuery(domain='api.example.com', query_type='A', source_tool='{tool}', sources=['{tool}']))\n")
        f.write(f"        record.traffic_http_metadata.append(NormalizedTrafficHTTPMetadata(host='api.example.com', method='GET', uri='/users', source_tool='{tool}', sources=['{tool}']))\n")
        f.write(f"        record.traffic_tls_metadata.append(NormalizedTrafficTLSMetadata(sni='api.example.com', tls_version='TLSv1.3', source_tool='{tool}', sources=['{tool}']))\n")
        f.write(f"        record.traffic_statistics.append(NormalizedTrafficStatistic(stat_name='Total Packets', stat_value='1000', source_tool='{tool}', sources=['{tool}']))\n")
        f.write("        return record\n")

