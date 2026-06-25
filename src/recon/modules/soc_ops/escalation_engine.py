from recon.modules.soc_ops.schema import IncidentModel


class EscalationEngine:
    """
    Evaluates incident priority and routes them to appropriate analyst queues based on severity.
    """

    def __init__(self):
        self.queues = {
            "immediate_escalation": [],
            "fast_response": [],
            "analyst_queue": [],
            "monitoring_queue": [],
        }

    def route_incident(self, incident: IncidentModel):
        if incident.severity == "critical":
            self.queues["immediate_escalation"].append(incident.incident_id)
        elif incident.severity == "high":
            self.queues["fast_response"].append(incident.incident_id)
        elif incident.severity == "medium":
            self.queues["analyst_queue"].append(incident.incident_id)
        else:
            self.queues["monitoring_queue"].append(incident.incident_id)
