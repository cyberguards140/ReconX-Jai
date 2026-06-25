import os
import subprocess
import time
import logging

class ProcessRunner:
    def __init__(self, job_tracker):
        self.job_tracker = job_tracker

    def run(self, job_id, command):
        self.job_tracker.update_status(job_id, "running")
        start_time = time.time()
        
        logging.info(f"Job {job_id} starting command: {command}")
        try:
            process = subprocess.Popen(
                command,
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Simple synchronous wait for demonstration
            # In a fully streaming setup, this would be async reading streams
            stdout, stderr = process.communicate()
            end_time = time.time()
            
            if process.returncode == 0:
                self.job_tracker.update_status(job_id, "completed")
            else:
                self.job_tracker.update_status(job_id, "failed")
                logging.error(f"Job {job_id} failed: {stderr}")
                
        except Exception as e:
            self.job_tracker.update_status(job_id, "failed")
            logging.error(f"Job {job_id} exception: {str(e)}")
