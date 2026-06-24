class ReconPipeline:
    def get_stages(self):
        return ["Subfinder", "Assetfinder", "Findomain", "Amass", "DNSX", "Httpx", "Naabu", "Nmap"]
