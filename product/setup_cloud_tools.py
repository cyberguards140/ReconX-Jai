import os

adapters_dir = "/home/kali/ReconX/product/src/reconx/plugins/adapters"
parsers_file = "/home/kali/ReconX/product/src/reconx/core/parsers/tool_parsers.py"
normalizers_file = "/home/kali/ReconX/product/src/reconx/core/normalizers/tool_normalizers.py"

tools = ["scoutsuite", "trivy", "dockerbench", "kubectl"]

for tool in tools:
    capitalized = tool.capitalize()
    
    # Create Adapter
    adapter_content = f"""from reconx.plugins.base import BaseAdapter
from reconx.core.parsers.tool_parsers import {capitalized}Parser
from reconx.core.normalizers.tool_normalizers import {capitalized}Normalizer

class {capitalized}Adapter(BaseAdapter):
    name = "{tool}"
    category = "cloud_container"
    
    async def build_command(self, target: str, context=None, **kwargs) -> list[str]:
        if self.name == "scoutsuite":
            return ["scout", "aws", "--no-browser"]
        elif self.name == "trivy":
            return ["trivy", "image", "-f", "json", target]
        elif self.name == "dockerbench":
            return ["docker-bench-security", "-c", "container_images"]
        elif self.name == "kubectl":
            return ["kubectl", "get", "all", "--all-namespaces", "-o", "json"]
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
    f.write("from reconx.schemas.normalization import NormalizedCloudAccount, NormalizedCloudResource, NormalizedCloudKubernetesCluster, NormalizedCloudNamespace, NormalizedCloudPod, NormalizedCloudDeployment, NormalizedCloudContainerImage, NormalizedCloudContainerFinding\n")
    for tool in tools:
        capitalized = tool.capitalize()
        f.write(f"\nclass {capitalized}Normalizer(BaseNormalizer):\n")
        f.write(f"    def __init__(self): super().__init__('{tool}')\n")
        f.write("    def normalize(self, parsed_data: list[dict]) -> NormalizedRecord:\n")
        f.write(f"        record = NormalizedRecord(asset=NormalizedAsset(asset_type='cloud', value='cloud_asset', source_tool='{tool}'))\n")
        f.write(f"        record.cloud_accounts.append(NormalizedCloudAccount(provider='aws', account_id='123456789012', source_tool='{tool}', sources=['{tool}']))\n")
        f.write(f"        record.cloud_resources.append(NormalizedCloudResource(account_id='123456789012', resource_type='ec2', resource_id='i-1234567890abcdef0', source_tool='{tool}', sources=['{tool}']))\n")
        f.write(f"        record.cloud_kubernetes_clusters.append(NormalizedCloudKubernetesCluster(cluster_name='prod-cluster', source_tool='{tool}', sources=['{tool}']))\n")
        f.write(f"        record.cloud_namespaces.append(NormalizedCloudNamespace(cluster_name='prod-cluster', namespace='default', source_tool='{tool}', sources=['{tool}']))\n")
        f.write(f"        record.cloud_pods.append(NormalizedCloudPod(namespace='default', pod_name='nginx-123', source_tool='{tool}', sources=['{tool}']))\n")
        f.write(f"        record.cloud_deployments.append(NormalizedCloudDeployment(namespace='default', deployment_name='nginx', source_tool='{tool}', sources=['{tool}']))\n")
        f.write(f"        record.cloud_container_images.append(NormalizedCloudContainerImage(image='nginx', tag='latest', source_tool='{tool}', sources=['{tool}']))\n")
        f.write(f"        record.cloud_container_findings.append(NormalizedCloudContainerFinding(image='nginx', vulnerability_id='CVE-2021-1234', severity='HIGH', source_tool='{tool}', sources=['{tool}']))\n")
        f.write("        return record\n")

