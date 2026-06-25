import subprocess


class RepairEngine:
    REPAIRS = {
        "subfinder": "go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest",
        "httpx": "go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest",
        "nuclei": "go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest",
        "katana": "go install github.com/projectdiscovery/katana/cmd/katana@latest",
        "naabu": "go install -v github.com/projectdiscovery/naabu/v2/cmd/naabu@latest",
        "dnsx": "go install -v github.com/projectdiscovery/dnsx/cmd/dnsx@latest",
        "gau": "go install github.com/lc/gau/v2/cmd/gau@latest",
        "waybackurls": "go install github.com/tomnomnom/waybackurls@latest",
        "assetfinder": "go install github.com/tomnomnom/assetfinder@latest",
        "chaos": "go install -v github.com/projectdiscovery/chaos-client/cmd/chaos@latest",
    }

    @staticmethod
    def repair(tool):
        if tool in RepairEngine.REPAIRS:
            cmd = RepairEngine.REPAIRS[tool]
            print(f"[*] Attempting to repair {tool} via: {cmd}")
            # Ensure GOPATH/bin is in PATH for successful go installs
            try:
                subprocess.run(cmd.split(), shell=False, check=True)
                return True
            except subprocess.CalledProcessError:
                return False
        return False

    @staticmethod
    def update_templates():
        print("[*] Updating Nuclei templates...")
        subprocess.run(["nuclei", "-update-templates"])
