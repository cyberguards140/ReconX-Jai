import os
import re

adapters_dir = "/home/kali/ReconX/product/src/reconx/plugins/adapters"
for fname in os.listdir(adapters_dir):
    if fname.endswith("_adapter.py") and fname != "base_adapter.py":
        filepath = os.path.join(adapters_dir, fname)
        with open(filepath, "r") as f:
            content = f.read()
        
        # fix def -> async def
        content = re.sub(r"def build_command", "async def build_command", content)
        content = re.sub(r"def parse_output", "async def parse_output", content)
        content = re.sub(r"def normalize", "async def normalize", content)
        
        # fix build_command signature
        content = re.sub(r"\(self, target: str, \*\*kwargs\)", "(self, target: str, context=None, **kwargs)", content)
        
        with open(filepath, "w") as f:
            f.write(content)

# Fix tests
tests_file = "/home/kali/ReconX/product/tests/test_network_recon.py"
with open(tests_file, "r") as f:
    content = f.read()

content = re.sub(r"def test_", "async def test_", content)
content = re.sub(r"adapter\.build_command", "await adapter.build_command", content)

# add pytest.mark.asyncio
import re
content = re.sub(r"async def test_", "@pytest.mark.asyncio\nasync def test_", content)
# clean up double markers
content = re.sub(r"@pytest.mark.asyncio\n@pytest.mark.asyncio", "@pytest.mark.asyncio", content)

with open(tests_file, "w") as f:
    f.write(content)
