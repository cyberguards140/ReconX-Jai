import logging
from typing import Any

from fastapi import HTTPException, Request, status

logger = logging.getLogger(__name__)


class TrustContext:
    def __init__(self, ip_address: str, user_agent: str, risk_score: float = 0.0):
        self.ip_address = ip_address
        self.user_agent = user_agent
        self.risk_score = risk_score


class ZeroTrustEvaluator:
    """
    Evaluates every request for context and risk, embodying "Never Trust, Always Verify".
    Even if a user has a valid JWT, their access may be blocked if their TrustContext
    is suspicious (e.g., impossible travel, unknown device, high risk score).
    """

    def __init__(self, max_risk_tolerance: float = 80.0):
        self.max_risk_tolerance = max_risk_tolerance

        # In a real deployment, these would be loaded from a threat intelligence feed or tenant policy
        self.banned_ips = set()
        self.suspicious_user_agents = {"curl", "python-requests", "nmap"}

    async def evaluate_request(self, request: Request, user_metadata: dict[str, Any] | None = None):
        """
        Evaluates the incoming HTTP request. Raises HTTPException if trust is broken.
        """
        ip = request.client.host if request.client else "0.0.0.0"
        user_agent = request.headers.get("user-agent", "").lower()

        # 1. IP Reputation Check
        if ip in self.banned_ips:
            logger.warning(f"Zero Trust blocked request from banned IP: {ip}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied by zero-trust policy (IP)",
            )

        # 2. Device/Agent Trust
        is_suspicious_agent = any(agent in user_agent for agent in self.suspicious_user_agents)
        if is_suspicious_agent:
            # We don't block outright, but we increase the risk score
            pass

        # 3. Dynamic Risk Scoring (Mocked logic)
        current_risk_score = 0.0
        if is_suspicious_agent:
            current_risk_score += 50.0

        if user_metadata and user_metadata.get("requires_mfa", False):
            # If the endpoint requires MFA but the token lacks the claim
            if not user_metadata.get("mfa_verified", False):
                current_risk_score += 100.0

        # 4. Final Policy Enforcement
        if current_risk_score >= self.max_risk_tolerance:
            logger.warning(
                f"Zero Trust blocked request due to high risk score: {current_risk_score}"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Session context risk too high. Re-authentication required.",
            )

        return TrustContext(ip_address=ip, user_agent=user_agent, risk_score=current_risk_score)


zero_trust_evaluator = ZeroTrustEvaluator()
