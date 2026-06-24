from typing import Dict, Any
from reconx.modules.executive_intel.risk_governance import RiskGovernanceEngine
from reconx.modules.executive_intel.kpi_engine import KPIEngine
from reconx.modules.executive_intel.portfolio_manager import PortfolioManager

class ExecutiveDashboard:
    """
    Synthesizes all governance data into a unified, high-level overview.
    """
    def __init__(self, risk_engine: RiskGovernanceEngine, kpi_engine: KPIEngine, portfolio: PortfolioManager):
        self.risk_engine = risk_engine
        self.kpi_engine = kpi_engine
        self.portfolio = portfolio

    def build_dashboard_view(self) -> Dict[str, Any]:
        """
        Gathers data from all executive engines for UI rendering.
        """
        return {
            "enterprise_risk_score": 75, # Conceptual aggregate
            "top_risks": [risk.model_dump() for risk in self.risk_engine.risk_register.values()],
            "kpis": self.kpi_engine.get_dashboard().model_dump(),
            "active_programs": [prog.model_dump() for prog in self.portfolio.programs.values()]
        }
