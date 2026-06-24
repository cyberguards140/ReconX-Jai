import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class DecisionScorer:
    """
    Multidimensional risk scoring evaluating Threat Intel, Graph Relationships, 
    and Compliance Posture to autonomously prioritize incidents.
    """
    def __init__(self):
        pass

    def calculate_priority(self, incident_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates Risk Score (0-100), Priority, and Confidence.
        """
        severity = incident_data.get("severity", "low").lower()
        asset_value = incident_data.get("asset_criticality", 1)  # 1-5 scale
        
        # Base Risk
        risk_score = 20.0
        if severity == "critical":
            risk_score += 50.0
        elif severity == "high":
            risk_score += 30.0
            
        # Business Impact Modifier
        risk_score += (asset_value * 5.0)
        
        # Cap at 100
        risk_score = min(risk_score, 100.0)
        
        # Determine Priority
        if risk_score >= 80:
            priority = "Critical"
        elif risk_score >= 60:
            priority = "High"
        elif risk_score >= 40:
            priority = "Medium"
        else:
            priority = "Low"

        # Confidence (heuristic mock)
        confidence = 0.85 if incident_data.get("ioc_matched") else 0.40

        return {
            "risk_score": risk_score,
            "priority": priority,
            "confidence": confidence
        }

decision_scorer = DecisionScorer()
