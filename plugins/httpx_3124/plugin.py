import asyncio
import json
import shutil

from core.paths import OUTPUTS_DIR
from core.plugin_interface import PluginInterface


class ToolAdapter(PluginInterface):
    async def execute(self, config: dict, context: dict) -> dict:
        target = context.get("target")
        if not target:
            raise ValueError("No target provided to httpx plugin")

        httpx_path = shutil.which("httpx")
        if not httpx_path:
            raise FileNotFoundError("httpx binary not found in PATH")

        project_dir = OUTPUTS_DIR / "projects" / target
        input_file = project_dir / "subdomains.txt"

        # If no subdomains.txt from previous step, we fallback to the raw target
        if not input_file.exists():
            input_file = project_dir / "target.txt"
            with open(input_file, "w") as f:
                f.write(f"{target}\n")

        out_file = project_dir / "httpx.json"

        # Execute httpx: -l input_file -title -tech-detect -status-code -json -o out_file
        cmd = [
            httpx_path,
            "-l",
            str(input_file),
            "-title",
            "-tech-detect",
            "-status-code",
            "-json",
            "-o",
            str(out_file),
            "-silent",
        ]

        process = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode != 0 and process.returncode is not None:
            raise RuntimeError(f"Httpx failed: {stderr.decode()}")

        live_hosts = []
        technologies = set()
        findings = []

        if out_file.exists():
            with open(out_file) as f:
                for line in f:
                    if not line.strip():
                        continue
                    try:
                        data = json.loads(line)
                        url = data.get("url")
                        if url:
                            live_hosts.append(url)

                        techs = data.get("tech", [])
                        for t in techs:
                            technologies.add(t)

                        findings.append(
                            {
                                "type": "web_host",
                                "url": url,
                                "status_code": data.get("status_code"),
                                "title": data.get("title"),
                                "technologies": techs,
                            }
                        )
                    except json.JSONDecodeError:
                        continue

        # Write alive urls for next steps (e.g., nuclei, katana)
        urls_file = project_dir / "alive_urls.txt"
        with open(urls_file, "w") as f:
            for url in live_hosts:
                f.write(f"{url}\n")

        return {
            "plugin": "httpx",
            "target": target,
            "live_hosts": len(live_hosts),
            "output_file": str(urls_file),
            "findings": findings,
        }
