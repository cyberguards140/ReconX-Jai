from ai.graph import AttackGraph
from ai.heuristics import HeuristicsEngine
from ai.memory.conversation import ConversationMemory
from ai.prioritization import PrioritizationEngine


class IntelligenceEngine:
    def __init__(self):
        self.memory = ConversationMemory()
        self.graph = AttackGraph()

    def process_raw_data(self, target: str, data: dict) -> dict:
        """Transforms raw output into structured intelligence."""
        report = {
            "target": target,
            "attack_surface": {"high_risk": [], "medium_risk": [], "low_risk": []},
            "recommendations": [],
        }

        # Subdomain Evaluation
        for sub in data.get("subdomains", []):
            self.graph.add_relationship(target, sub)
            risk = HeuristicsEngine.evaluate_subdomain(sub)
            if risk == "HIGH":
                report["attack_surface"]["high_risk"].append(sub)
            elif risk == "LOW":
                report["attack_surface"]["low_risk"].append(sub)
            else:
                report["attack_surface"]["medium_risk"].append(sub)

        # Service Evaluation
        for port in data.get("ports", []):
            risk_label = HeuristicsEngine.evaluate_service(port, data.get("tech_stack", []))
            if "HIGH" in risk_label:
                report["attack_surface"]["high_risk"].append(f"Port {port}")

        # Next Best Actions
        report["recommendations"] = PrioritizationEngine.generate_next_actions(
            report["attack_surface"]["high_risk"]
        )

        return report


import logging
import os
from typing import Any

import aiohttp

logger = logging.getLogger(__name__)


class AIEngine:
    """
    Core AI Wrapper integrating LLMs for executive intelligence synthesis.
    Defaults to OpenAI compatible APIs.
    """

    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY", "")
        self.api_url = "https://api.openai.com/v1/chat/completions"
        self.model = "gpt-4o"

    async def synthesize_finding(self, finding_data: dict[str, Any]) -> str:
        """
        Takes raw vulnerability data and returns a human-readable mitigation report.
        """
        if not self.api_key:
            return "AI Analysis unavailable. Missing OPENAI_API_KEY environment variable."

        prompt = f"""
        You are a senior cybersecurity architect. Review the following vulnerability finding 
        and provide a concise, executive-level summary and actionable remediation strategy.
        Focus on blast radius and real-world impact.
        
        Finding Data:
        {finding_data}
        """

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a senior security expert."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
        }

        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.api_url, json=payload, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data["choices"][0]["message"]["content"]
                    else:
                        logger.error(f"AI API Error: {response.status}")
                        return "AI Analysis failed due to API error."
        except Exception as e:
            logger.error(f"AI Engine Exception: {e}")
            return "AI Analysis failed due to internal exception."


ai_engine = AIEngine()
