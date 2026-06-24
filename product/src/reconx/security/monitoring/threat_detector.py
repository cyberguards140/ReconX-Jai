import logging
from collections import defaultdict
import time
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ThreatDetector:
    """
    Analyzes streams of security and audit events to detect anomalies,
    such as Impossible Travel, Credential Stuffing, or Privilege Escalation.
    """
    def __init__(self):
        # Extremely basic in-memory windowing. 
        # In production, this would use Redis for sliding window rate limits or Kafka Streams/Flink.
        self.failed_logins: Dict[str, list] = defaultdict(list)
        
    def analyze_event(self, event: Dict[str, Any]):
        """
        Ingests an event from the audit stream and evaluates it against threat heuristics.
        """
        action = event.get("action")
        user_id = event.get("user_id")
        
        if not user_id:
            return

        if action == "auth_failed":
            self._handle_auth_failure(user_id)
        elif action == "auth_success":
            self._handle_auth_success(user_id)
            
    def _handle_auth_failure(self, user_id: str):
        now = time.time()
        # Keep failures in the last 5 minutes (300s)
        self.failed_logins[user_id] = [t for t in self.failed_logins[user_id] if now - t < 300]
        self.failed_logins[user_id].append(now)
        
        # If > 5 failures in 5 minutes
        if len(self.failed_logins[user_id]) >= 5:
            self._generate_alert("BruteForceDetection", f"User {user_id} had 5+ failed login attempts in 5 minutes.")

    def _handle_auth_success(self, user_id: str):
        # Clear failures on success
        if user_id in self.failed_logins:
            del self.failed_logins[user_id]
            
    def _generate_alert(self, alert_type: str, message: str):
        """
        Forwards the generated alert to the SOC Platform or Alertmanager.
        """
        logger.error(f"SECURITY_ALERT [{alert_type}]: {message}")
        # Send to SOC API or Kafka Topic 'security.alerts'

threat_detector = ThreatDetector()
