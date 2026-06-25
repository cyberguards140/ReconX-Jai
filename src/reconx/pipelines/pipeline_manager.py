PIPELINES = {
    "Quick Recon": ["subfinder", "dnsx", "httpx"],
    "Deep Recon": ["subfinder", "amass", "dnsx", "httpx", "naabu", "nmap"],
    "Infrastructure Discovery": ["whois", "asn", "reverse_dns", "dnsx"],
    "OSINT Recon": ["shodan", "theharvester", "whois"],
    "Quick Scan": ["nuclei", "sslscan"],
    "Web Assessment": ["nikto", "nuclei", "testssl"],
    "Deep Assessment": ["nessus", "nuclei", "openvas"],
    "SSL Assessment": ["sslscan", "testssl"],
    "Quick Web Discovery": ["katana", "httpx", "linkfinder"],
    "Content Discovery": ["ffuf", "dirsearch", "feroxbuster"],
    "Historical Discovery": ["waybackurls", "gau"],
    "Deep Web Enumeration": ["katana", "ffuf", "linkfinder", "secretfinder", "jsfinder"],
    "Storage Discovery": ["cloud_discovery", "storage_discovery", "exposure_analysis"],
    "Cloud Asset Mapping": ["dnsx", "cloud_fingerprint", "asset_correlation"],
    "Cloud Exposure Discovery": ["storage_discovery", "permissions", "exposure_detection"],
    "Full Cloud Enumeration": [
        "cloud_discovery",
        "storage_discovery",
        "iam_discovery",
        "relationships",
        "risk_analysis",
    ],
}


class PipelineManager:
    active_pipelines = {}

    @classmethod
    def get_pipelines(cls):
        return [{"name": k, "tools": v} for k, v in PIPELINES.items()]

    @classmethod
    def start_pipeline(cls, name, project_id, target):
        if name not in PIPELINES:
            return None
        tools = PIPELINES[name]
        if not tools:
            return None

        first_tool = tools[0]
        # In MVP, we use the standard execution engine
        from core.argument_engine import ArgumentEngine
        from core.config_manager import ConfigManager
        from core.execution_engine import ExecutionEngine

        cfg = ConfigManager.load_config(first_tool)
        cmd = ArgumentEngine.generate_command(first_tool, target, cfg)

        job_id = ExecutionEngine.queue_job(first_tool, project_id, target, cmd)
        cls.active_pipelines[job_id] = {
            "name": name,
            "project_id": project_id,
            "target": target,
            "step": 0,
        }
        return job_id

    @classmethod
    def handle_job_completion(cls, job_id):
        if job_id not in cls.active_pipelines:
            return

        pipeline = cls.active_pipelines.pop(job_id)
        name = pipeline["name"]
        tools = PIPELINES[name]
        step = pipeline["step"]

        next_step = step + 1
        if next_step < len(tools):
            next_tool = tools[next_step]
            # Fetch targets from inventory or pass through previous target
            target = pipeline["target"]
            # To be truly dynamic, here we would pull newly discovered assets
            # (e.g. from subfinder) and pass them to DNSX.
            # For MVP orchestration, we just keep passing the root target
            # since tools typically resolve internal inputs or read from files
            # (assuming output integration).

            from core.argument_engine import ArgumentEngine
            from core.config_manager import ConfigManager
            from core.execution_engine import ExecutionEngine

            cfg = ConfigManager.load_config(next_tool)
            cmd = ArgumentEngine.generate_command(next_tool, target, cfg)

            new_job_id = ExecutionEngine.queue_job(next_tool, pipeline["project_id"], target, cmd)
            cls.active_pipelines[new_job_id] = {
                "name": name,
                "project_id": pipeline["project_id"],
                "target": target,
                "step": next_step,
            }
