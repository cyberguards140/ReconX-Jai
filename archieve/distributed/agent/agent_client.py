import time
import json
from distributed.registry.node_registry import NodeRegistry
from distributed.health.health_monitor import HealthMonitor

class AgentClient:
    def __init__(self, hostname, agent_type, token):
        self.hostname = hostname
        self.agent_type = agent_type
        self.token = token
        self.node_id = None

    def connect(self):
        print(f"[{self.hostname}] Authenticating...")
        self.node_id = NodeRegistry.register_node(self.hostname, self.agent_type, self.token)
        print(f"[{self.hostname}] Connected. Node ID: {self.node_id}")

    def send_heartbeat(self):
        # Simulated metrics
        cpu = 45.0
        ram = 60.0
        disk = 30.0
        latency = 15.0
        state = HealthMonitor.process_heartbeat(self.node_id, cpu, ram, disk, latency)
        print(f"[{self.hostname}] Heartbeat sent. State: {state}")
