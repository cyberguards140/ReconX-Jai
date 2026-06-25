import logging
import os
import sys

from flask import Flask, send_from_directory
from flask_sock import Sock

# Make sure we can import from backend
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from core.scheduler import Scheduler
from dashboard.backend.api import api_bp
from dashboard.backend.websocket import setup_websocket

app = Flask(__name__, static_folder="../frontend")
app.register_blueprint(api_bp)
sock = Sock(app)
setup_websocket(sock)

# Setup logging
log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

dashboard_logger = logging.getLogger("dashboard")
dashboard_logger.setLevel(logging.INFO)

# Ensure logs dir exists
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
log_dir = os.path.join(base_dir, "logs")
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

fh = logging.FileHandler(os.path.join(log_dir, "dashboard.log"))
fh.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
dashboard_logger.addHandler(fh)


@app.route("/")
def index():
    dashboard_logger.info("Dashboard loaded")
    return send_from_directory("../frontend", "reconx-dashboard-v2.html")


@app.route("/<path:path>")
def static_files(path):
    return send_from_directory("../frontend", path)


def run_server(port=3000):
    dashboard_logger.info("Starting Execution Scheduler...")
    Scheduler.start()
    dashboard_logger.info("Dashboard Server Started")
    app.run(host="127.0.0.1", port=port, use_reloader=False)


if __name__ == "__main__":
    run_server(3000)
