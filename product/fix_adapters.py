import os

adapters_dir = "/home/kali/ReconX/product/src/reconx/plugins/adapters"
for fname in os.listdir(adapters_dir):
    if fname.endswith("_adapter.py") and fname != "base_adapter.py":
        filepath = os.path.join(adapters_dir, fname)
        with open(filepath, "r") as f:
            content = f.read()
        
        if "async def validate" not in content:
            new_methods = """
    async def validate(self) -> bool:
        return True

    async def save_results(self, scan_id: str, raw_output: str):
        pass
"""
            content += new_methods
            with open(filepath, "w") as f:
                f.write(content)
