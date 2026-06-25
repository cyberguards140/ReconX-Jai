from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from core.auth.middleware import SecurityMiddleware
from attack_surface.assets.attack_models.simulator import attack_simulator
from attack_surface.assets.forecasting.risk_predictor import risk_forecaster
from attack_surface.assets.governance.tracker import simulation_tracker
from attack_surface.assets.scenarios.what_if import what_if_engine
from attack_surface.assets.twin_engine.modeler import twin_modeler
from plugins.enterprise.isolation.tenant_context import get_current_tenant_id

router = APIRouter(tags=["Cyber Digital Twin"], dependencies=[Depends(SecurityMiddleware)])


class SimulationRequest(BaseModel):
    actor_profile: str = "ransomware"


class WhatIfRequest(BaseModel):
    theoretical_changes: list[dict[str, Any]]


class ForecastRequest(BaseModel):
    horizon_days: int = 30
    current_risk_score: float = 50.0
    exposure_growth_rate: float = 0.05


@router.post("/simulate", summary="Run a theoretical attack simulation")
async def run_simulation(request: SimulationRequest):
    """
    Builds a Digital Twin Snapshot and executes an attack campaign against it.
    """
    tenant_id = get_current_tenant_id()
    if not tenant_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Tenant context missing"
        )

    snapshot = twin_modeler.build_snapshot()
    results = attack_simulator.simulate_campaign(snapshot, request.actor_profile)

    simulation_tracker.log_simulation(f"attack_sim_{request.actor_profile}", {}, results)

    return {"message": "Simulation Complete", "results": results}


@router.post("/scenario", summary="Execute a What-If Scenario")
async def run_what_if_scenario(request: WhatIfRequest):
    """
    Injects theoretical architecture changes into the twin and evaluates the risk impact.
    """
    snapshot = twin_modeler.build_snapshot()
    results = what_if_engine.run_scenario(snapshot, request.theoretical_changes)

    simulation_tracker.log_simulation("what_if_scenario", request.theoretical_changes, results)

    return {"message": "Scenario Evaluated", "results": results}


@router.post("/forecast", summary="Forecast future business impact")
async def run_forecast(request: ForecastRequest):
    """
    Projects risk and potential financial impact out across a given time horizon.
    """
    results = risk_forecaster.generate_forecast(
        request.current_risk_score, request.exposure_growth_rate, request.horizon_days
    )

    simulation_tracker.log_simulation("risk_forecast", request.dict(), results)

    return {"message": "Forecast Generated", "forecast": results}
