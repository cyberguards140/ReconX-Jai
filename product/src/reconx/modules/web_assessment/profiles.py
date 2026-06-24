from enum import Enum
from typing import List

class AssessmentProfile(str, Enum):
    QUICK = "quick"
    STANDARD = "standard"
    DEEP = "deep"

def get_assessment_tools(profile: AssessmentProfile) -> List[dict]:
    if profile == AssessmentProfile.QUICK:
        return [
            {"id": "nikto", "plugin": "nikto", "depends_on": []}
        ]
    elif profile == AssessmentProfile.STANDARD:
        return [
            {"id": "nikto", "plugin": "nikto", "depends_on": []},
            {"id": "sslscan", "plugin": "sslscan", "depends_on": []}
        ]
    elif profile == AssessmentProfile.DEEP:
        return [
            {"id": "nikto", "plugin": "nikto", "depends_on": []},
            {"id": "sslscan", "plugin": "sslscan", "depends_on": []},
            {"id": "testssl", "plugin": "testssl", "depends_on": ["sslscan"]}
        ]
    return []
