from dashboard.backend.websocket import broadcast


class OutputStreamer:
    @staticmethod
    def stream(job_id, tool_id, output_type, content):
        # Broadcast to dashboard terminal
        msg = {
            "type": "terminal_output",
            "job_id": job_id,
            "tool_id": tool_id,
            "output_type": output_type,
            "content": content,
        }
        broadcast(msg)

    @staticmethod
    def status_update(job_id, tool_id, status):
        msg = {"type": "job_status", "job_id": job_id, "tool_id": tool_id, "status": status}
        broadcast(msg)
