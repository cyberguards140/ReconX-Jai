from typing import Dict, Any, List

class ComplianceMapper:
    """
    Maps raw vulnerability data and exposures to Enterprise Compliance Frameworks.
    """
    def __init__(self):
        # MVP In-memory Matrices
        self.matrices = {
            "ISO27001": {
                "A.12.6.1": {"description": "Management of Technical Vulnerabilities", "triggers": ["critical", "high"]},
                "A.13.1.1": {"description": "Network Controls (Exposure)", "triggers": ["critical_exposure"]},
                "A.14.2.5": {"description": "Secure System Engineering Principles", "triggers": ["medium", "low"]}
            },
            "SOC2": {
                "CC7.1": {"description": "Vulnerability Management", "triggers": ["critical", "high"]},
                "CC6.6": {"description": "External Boundaries", "triggers": ["critical_exposure"]}
            }
        }

    def generate_gap_report(self, framework: str, findings: List[Dict[str, Any]], exposures: List[Dict[str, Any]]) -> str:
        """
        Generates a markdown compliance gap report based on current data.
        """
        matrix = self.matrices.get(framework.upper())
        if not matrix:
            return f"# Error\nFramework {framework} is not supported."

        report = f"# {framework.upper()} Compliance Gap Report\n\n"
        
        for control, details in matrix.items():
            report += f"## Control {control}: {details['description']}\n"
            
            control_failures = 0
            
            # Map Vulns
            for finding in findings:
                if finding.get("severity", "").lower() in details["triggers"]:
                    report += f"- ❌ **Gap**: {finding.get('title')} on `{finding.get('asset_target')}`\n"
                    control_failures += 1
            
            # Map Exposures
            if "critical_exposure" in details["triggers"]:
                for exp in exposures:
                    if exp.get("is_critical_exposure"):
                        report += f"- ❌ **Gap**: Exposed Portal ({', '.join(exp.get('exposure_tags', []))}) on `{exp.get('target')}`\n"
                        control_failures += 1
                        
            if control_failures == 0:
                report += "- ✅ **Compliant**: No gaps detected for this control.\n"
                
            report += "\n"
            
        return report

compliance_mapper = ComplianceMapper()
