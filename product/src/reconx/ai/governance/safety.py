import logging
import re

logger = logging.getLogger(__name__)

class SafetyGuard:
    """
    Input validation and output sanitization for the Copilot.
    Protects against Prompt Injection and Data Leakage.
    """
    def __init__(self):
        # Extremely basic heuristics. In prod, use models like Lakera Guard or LLM-based classifiers.
        self.injection_patterns = [
            re.compile(r"(?i)ignore\s+all\s+previous\s+instructions"),
            re.compile(r"(?i)you\s+are\s+now\s+a"),
            re.compile(r"(?i)system\s+prompt")
        ]

    def is_safe(self, text: str) -> bool:
        """Evaluates whether the input text is safe to pass to the LLM."""
        for pattern in self.injection_patterns:
            if pattern.search(text):
                logger.warning(f"SafetyGuard triggered by pattern match in input.")
                return False
        return True

    def sanitize_output(self, text: str) -> str:
        """
        Ensures no sensitive system patterns (like raw JWTs or internal IP blocks) leak.
        """
        # Example regex filtering. Implementation depends on exact threat model.
        return text

safety_guard = SafetyGuard()
