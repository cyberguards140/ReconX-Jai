import subprocess
import threading
import os
import signal
import shlex
from core.legacy_core.output_streamer import OutputStreamer
from core.legacy_core.job_manager import JobManager
from core.legacy_core.parser_engine import ParserEngine
from platform_core.task_engine.pipelines.pipeline_manager import PipelineManager

class ProcessManager:
    active_processes = {}

    @classmethod
    def run_process(cls, job_id, tool_id, command_string):
        def _read_stream(stream, output_type, project_id, target):
            for line in iter(stream.readline, b''):
                decoded = line.decode('utf-8', errors='replace').rstrip()
                OutputStreamer.stream(job_id, tool_id, output_type, decoded)
                JobManager.log_output(job_id, output_type, decoded)
                if output_type == "stdout":
                    ParserEngine.parse(tool_id, project_id, target, decoded)
            stream.close()

        def _run():
            cmd = shlex.split(command_string)
            try:
                proc = subprocess.Popen(
                    cmd, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    bufsize=1, # Line buffered
                    preexec_fn=os.setsid # Allow killing process groups
                )
                cls.active_processes[job_id] = proc
                JobManager.update_status(job_id, "running", proc.pid)
                OutputStreamer.status_update(job_id, tool_id, "running")

                job_meta = JobManager.get_job(job_id)
                proj = job_meta["project_id"] if job_meta else ""
                tgt = job_meta["target"] if job_meta else ""

                t_out = threading.Thread(target=_read_stream, args=(proc.stdout, "stdout", proj, tgt))
                t_err = threading.Thread(target=_read_stream, args=(proc.stderr, "stderr", proj, tgt))
                t_out.start()
                t_err.start()

                proc.wait()
                t_out.join()
                t_err.join()

                if job_id in cls.active_processes:
                    del cls.active_processes[job_id]
                
                # Check if it was cancelled
                current_job = JobManager.get_job(job_id)
                if current_job and current_job["status"] != "cancelled":
                    final_status = "completed" if proc.returncode == 0 else "failed"
                    JobManager.update_status(job_id, final_status)
                    OutputStreamer.status_update(job_id, tool_id, final_status)
                
                from core.legacy_core.result_handler import ResultHandler
                ResultHandler.save_results(job_id)
                PipelineManager.handle_job_completion(job_id)

            except Exception as e:
                JobManager.update_status(job_id, "failed")
                OutputStreamer.stream(job_id, tool_id, "stderr", f"Execution error: {str(e)}")
                OutputStreamer.status_update(job_id, tool_id, "failed")

        t = threading.Thread(target=_run)
        t.start()

    @classmethod
    def stop_process(cls, job_id):
        proc = cls.active_processes.get(job_id)
        if proc:
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
                JobManager.update_status(job_id, "cancelled")
                OutputStreamer.status_update(job_id, "tool", "cancelled")
                del cls.active_processes[job_id]
                return True
            except Exception as e:
                pass
        # Fallback if queued but not running
        JobManager.update_status(job_id, "cancelled")
        return True
