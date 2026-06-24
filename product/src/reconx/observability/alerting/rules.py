import yaml
import os

ALERT_RULES = {
    "groups": [
        {
            "name": "ReconX_API_Alerts",
            "rules": [
                {
                    "alert": "HighAPIErrorRate",
                    "expr": 'rate(reconx_http_requests_total{status_code=~"5.."}[5m]) / rate(reconx_http_requests_total[5m]) > 0.05',
                    "for": "5m",
                    "labels": {"severity": "critical"},
                    "annotations": {
                        "summary": "High API Error Rate (> 5%)",
                        "description": "More than 5% of API requests are returning 5xx errors across the last 5 minutes."
                    }
                },
                {
                    "alert": "HighAPILatency",
                    "expr": 'histogram_quantile(0.95, rate(reconx_http_request_duration_seconds_bucket[5m])) > 1.0',
                    "for": "5m",
                    "labels": {"severity": "warning"},
                    "annotations": {
                        "summary": "High API Latency (p95 > 1s)",
                        "description": "The 95th percentile of API request latency is exceeding 1 second."
                    }
                }
            ]
        },
        {
            "name": "ReconX_Workflow_Alerts",
            "rules": [
                {
                    "alert": "WorkflowFailureSpike",
                    "expr": 'rate(reconx_workflow_executions_total{status="failed"}[10m]) > 10',
                    "for": "5m",
                    "labels": {"severity": "critical"},
                    "annotations": {
                        "summary": "Spike in Workflow Failures",
                        "description": "The workflow execution failure rate is abnormally high."
                    }
                }
            ]
        }
    ]
}

def generate_prometheus_alerts(output_path: str = "/app/config/prometheus_rules.yml"):
    """
    Dumps the canonical Alerting Rules for Prometheus Alertmanager.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        yaml.dump(ALERT_RULES, f, default_flow_style=False)
