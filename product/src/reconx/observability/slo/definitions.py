import json
import os

SLO_DEFINITIONS = [
    {
        "service": "api-gateway",
        "slo": "API Availability",
        "objective": 99.9,
        "indicator": "Percentage of successful non-5xx responses over a rolling 30-day window",
        "query_success": 'sum(rate(reconx_http_requests_total{status_code!~"5.."}[30d]))',
        "query_total": 'sum(rate(reconx_http_requests_total[30d]))'
    },
    {
        "service": "api-gateway",
        "slo": "API Latency",
        "objective": 95.0,
        "indicator": "Percentage of requests completing under 150ms over a rolling 7-day window",
        "query_success": 'sum(rate(reconx_http_request_duration_seconds_bucket{le="0.15"}[7d]))',
        "query_total": 'sum(rate(reconx_http_request_duration_seconds_count[7d]))'
    },
    {
        "service": "workflow-engine",
        "slo": "Workflow Success Rate",
        "objective": 99.0,
        "indicator": "Percentage of successfully completed workflows vs total started",
        "query_success": 'sum(rate(reconx_workflow_executions_total{status="success"}[30d]))',
        "query_total": 'sum(rate(reconx_workflow_executions_total[30d]))'
    }
]

def generate_slo_dashboard(output_path: str = "/app/config/slos.json"):
    """
    Dumps the SLO definitions which can be consumed by Grafana SLO generators or custom executive dashboards.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(SLO_DEFINITIONS, f, indent=4)
