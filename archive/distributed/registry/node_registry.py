from core.distributed_db import SessionLocal, Node, Agent
from dashboard.backend.websocket import broadcast

class NodeRegistry:
    @staticmethod
    def register_node(hostname, node_type, token):
        db = SessionLocal()
        node = db.query(Node).filter(Node.hostname == hostname).first()
        if not node:
            node = Node(hostname=hostname, node_type=node_type, status="Online")
            db.add(node)
            db.commit()
            db.refresh(node)
            
            agent = Agent(node_id=node.id, auth_token=token, version="1.0.0")
            db.add(agent)
            db.commit()
            
            broadcast({
                "type": "node_registered",
                "hostname": hostname,
                "node_id": node.id
            })
        db.close()
        return node.id if node else None

    @staticmethod
    def list_nodes():
        db = SessionLocal()
        nodes = db.query(Node).all()
        res = [{"id": n.id, "hostname": n.hostname, "status": n.status, "type": n.node_type} for n in nodes]
        db.close()
        return res
