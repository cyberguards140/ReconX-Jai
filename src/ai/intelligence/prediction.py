import logging
from typing import Dict, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class ExposurePredictionEngine:
    """
    Phase 51: Predictive Forecasting.
    Uses statistical heuristics to predict future exposure events.
    """
    def __init__(self):
        pass

    def forecast_risk(self, asset: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates the probability of an asset becoming a critical exposure in the near future.
        """
        forecasts = []
        
        # 1. Certificate Expiration Prediction
        cert = asset.get("certificate", {})
        if cert.get("expiration_date"):
            try:
                exp_date = datetime.fromisoformat(cert["expiration_date"])
                days_until_exp = (exp_date - datetime.utcnow()).days
                if 0 < days_until_exp <= 14:
                    forecasts.append(f"HIGH PROBABILITY OUTAGE: Certificate expires in {days_until_exp} days.")
            except ValueError:
                pass

        # 2. Technology Vulnerability Trend Prediction
        tech_stack = asset.get("technologies", [])
        high_risk_techs = ["jenkins", "gitlab", "confluence", "exchange"]
        for tech in tech_stack:
            if tech.lower() in high_risk_techs:
                forecasts.append(f"ELEVATED RISK TREND: {tech} historically receives critical CVEs frequently. Monitor closely.")
                
        if forecasts:
            logger.warning(f"[Prediction Engine] Forecasts generated for {asset.get('target')}: {forecasts}")
            
        return {"target": asset.get("target"), "forecasts": forecasts}

prediction_engine = ExposurePredictionEngine()
