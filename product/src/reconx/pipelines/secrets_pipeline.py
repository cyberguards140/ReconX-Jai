class SecretsPipeline:
    def get_stages(self):
        return ["GitLeaks", "TruffleHog"]
