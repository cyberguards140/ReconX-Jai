from core.distributed_db import SessionLocal, NodeHealth, Node
from dashboard.backend.websocket import broadcast
from datetime import datetime

class HealthMonitor:
    @staticmethod
    def process_heartbeat(node_id, cpu, ram, disk, latency):
        db = SessionLocal()
        state = "Healthy"
        if cpu > 85 or ram > 90:
            state = "Warning"
        if cpu > 98 or latency > 1000:
            state = "Critical"
            
        health = NodeHealth(
            node_id=node_id,
            cpu_usage=cpu,
            ram_usage=ram,
            disk_usage=disk,
            network_latency=latency,
            health_state=state
        )
        db.add(health)
        db.commit()
        
        # Check node status update
        node = db.query(Node).filter(Node.id == node_id).first()
        if node and state == "Critical":
            broadcast({
                "type": "health_alert",
                "hostname": node.hostname,
                "state": state
            })
            
        db.close()
        return state
