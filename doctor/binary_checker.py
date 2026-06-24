import shutil
import subprocess

class BinaryChecker:
    @staticmethod
    def check_binary(tool_name):
        path = shutil.which(tool_name)
        if not path:
            return {"tool": tool_name, "installed": False, "version": "unknown"}
        
        # Try to get version
        try:
            res = subprocess.run([tool_name, "-version"], capture_output=True, text=True, timeout=2)
            if res.returncode != 0:
                res = subprocess.run([tool_name, "--version"], capture_output=True, text=True, timeout=2)
            output = res.stdout.strip() or res.stderr.strip()
            version = output.split('\n')[0][:30] if output else "installed"
        except Exception:
            version = "installed"
            
        return {"tool": tool_name, "installed": True, "version": version}

    @staticmethod
    def check_all():
        tools = ["subfinder", "amass", "assetfinder", "chaos", "dnsx", "httpx", "naabu", "masscan", "nmap", "whois", "theHarvester",
                 "nuclei", "nikto", "sslscan", "testssl",
                 "ffuf", "dirsearch", "feroxbuster", "gobuster", "katana", "hakrawler", "gau", "waybackurls", "linkfinder"]
        
        results = []
        for t in tools:
            results.append(BinaryChecker.check_binary(t))
        return results
