from core.plugin_db import SessionLocal, ConnectorRegistry
import json

class ConnectorFramework:
    @staticmethod
    def register_connector(connector_name, category, config_dict):
        db = SessionLocal()
        c = db.query(ConnectorRegistry).filter(ConnectorRegistry.connector_name == connector_name).first()
        if not c:
            c = ConnectorRegistry(connector_name=connector_name, category=category, enabled=True, config=json.dumps(config_dict))
            db.add(c)
        else:
            c.config = json.dumps(config_dict)
        db.commit()
        db.close()

    @staticmethod
    def dispatch_payload(connector_name, payload):
        db = SessionLocal()
        c = db.query(ConnectorRegistry).filter(ConnectorRegistry.connector_name == connector_name, ConnectorRegistry.enabled == True).first()
        if c:
            print(f"[ConnectorFramework] Dispatching to {connector_name}: {payload}")
        db.close()
