from typing import Dict, Any, Optional
from reconx.modules.security_analytics.schema import AlertModel
from reconx.modules.security_analytics.event_normalizer import EventNormalizer
from reconx.modules.security_analytics.detection_engine import DetectionEngine
from reconx.modules.security_analytics.behavior_engine import BehaviorEngine
from reconx.modules.security_analytics.correlation_engine import CorrelationEngine
from reconx.modules.security_analytics.alert_engine import AlertEngine
from reconx.modules.security_analytics.investigation_engine import InvestigationEngine

class SecurityAnalyticsEngine:
    """
    Master orchestrator routing incoming events through the analytics pipeline.
    """
    def __init__(self):
        self.normalizer = EventNormalizer()
        self.detection = DetectionEngine()
        self.behavior = BehaviorEngine()
        self.correlation = CorrelationEngine(self.behavior)
        self.alerter = AlertEngine()
        self.investigator = InvestigationEngine()

    def process_event(self, raw_event: Dict[str, Any], threat_context: Dict[str, Any] = None) -> Optional[AlertModel]:
        """
        Full pipeline: Normalize -> Behavior Baseline -> Detection -> Correlation -> Alerting
        """
        norm_event = self.normalizer.normalize(raw_event)
        
        self.behavior.update_baseline(norm_event)
        
        rule_triggered = self.detection.evaluate_event(norm_event)
        
        score = self.correlation.correlate_event(norm_event, threat_context)
        
        # Conceptually, if a rule triggers or score is very high, generate alert
        if rule_triggered or score > 60:
            return self.alerter.generate_alert(score, norm_event)
            
        return None
