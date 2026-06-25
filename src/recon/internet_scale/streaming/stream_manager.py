import asyncio

from .log_writer import LogWriter
from .progress_tracker import progress_tracker
from .terminal_stream import TerminalStream


class StreamManager:
    async def stream_output(self, process, job_id, tool, project):
        log_writer = LogWriter(project, job_id)

        async def read_stdout():
            while True:
                line = await process.stdout.readline()
                if not line:
                    break
                decoded_line = line.decode("utf-8").rstrip()
                log_writer.write_stdout(decoded_line)
                await TerminalStream.broadcast_output(job_id, "stdout", decoded_line)
                await progress_tracker.process_line(job_id, tool, decoded_line)

        async def read_stderr():
            while True:
                line = await process.stderr.readline()
                if not line:
                    break
                decoded_line = line.decode("utf-8").rstrip()
                log_writer.write_stderr(decoded_line)
                await TerminalStream.broadcast_output(job_id, "stderr", decoded_line)

        await asyncio.gather(read_stdout(), read_stderr())
