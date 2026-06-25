import json

from .event_dispatcher import event_dispatcher
from .parsers.nmap_parser import NmapParser
from .parsers.nuclei_parser import NucleiParser


class ProgressTracker:
    def __init__(self):
        self.parsers = {"nmap": NmapParser, "nuclei": NucleiParser}

    async def process_line(self, job_id, tool, line):
        parser = self.parsers.get(tool)
        if parser:
            progress_data = parser.parse(line)
            if progress_data:
                event = {"type": "progress", "job_id": job_id, "progress": progress_data}
                await event_dispatcher.dispatch("/ws/progress", json.dumps(event))


progress_tracker = ProgressTracker()
