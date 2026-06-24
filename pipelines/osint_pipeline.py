class OsintPipeline:
    def get_stages(self):
        return ["SecurityTrails", "CRTSH", "Shodan", "TheHarvester"]
