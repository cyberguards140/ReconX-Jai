class VulnPipeline:
    def get_stages(self):
        return ["Httpx", "Nuclei", "Nikto", "Dalfox", "SSLScan"]
