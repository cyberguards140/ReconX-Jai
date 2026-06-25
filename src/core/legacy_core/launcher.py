import logging
import threading
import webbrowser

from flask import Flask, send_from_directory

app = Flask(__name__)
# Suppress flask output
log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)


@app.route("/")
def index():
    return send_from_directory("../dashboard", "reconx-dashboard-v2.html")


@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory("../dashboard", path)


class DashboardLauncher:
    def __init__(self, port=3000, auto_open=True):
        self.port = port
        self.auto_open = auto_open
        self.server_thread = None

    def start(self):
        if self.server_thread is None or not self.server_thread.is_alive():
            self.server_thread = threading.Thread(target=self._run_server, daemon=True)
            self.server_thread.start()
            print(f"\n[+] Dashboard server started on http://localhost:{self.port}")
            if self.auto_open:
                try:
                    webbrowser.open(f"http://localhost:{self.port}")
                except Exception:
                    pass
        else:
            print("\n[!] Dashboard is already running.")

    def _run_server(self):
        app.run(host="127.0.0.1", port=self.port, use_reloader=False)

    def stop(self):
        pass
