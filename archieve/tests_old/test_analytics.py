import pytest
from reconx.modules.analytics.scoring import RiskScoringModel
from reconx.modules.analytics.risk_engine import AnalyticsRiskEngine
from reconx.modules.analytics.correlation_engine import AnalyticsCorrelationEngine
from reconx.modules.analytics.prioritization import AssetPrioritization
from reconx.modules.analytics.recommendations import RecommendationGenerator
from reconx.services.analytics_engine import AnalyticsEngine

def test_risk_scoring_base():
    # 1 critical (25), 1 high (10), 1 medium (5) = 40
    score = RiskScoringModel.compute_base_score(1, 1, 1)
    assert score == 40.0

def test_analytics_risk_engine():
    # Base 40, High Criticality (+0.5), External (+0.5) => multiplier 2.0
    score = AnalyticsRiskEngine.calculate_weighted_risk(1, 1, 1, "High", "External")
    assert score == 80.0

def test_analytics_correlation_engine():
    findings = [
        {"asset_id": "a1", "title": "Vuln A", "sources": ["s1"]},
        {"asset_id": "a1", "title": "Vuln A", "sources": ["s2"]},
        {"asset_id": "a2", "title": "Vuln B", "sources": ["s1"]}
    ]
    merged = AnalyticsCorrelationEngine.merge_finding_duplicates(findings)
    assert len(merged) == 2
    merged_a1 = next(f for f in merged if f["asset_id"] == "a1")
    assert len(merged_a1["sources"]) == 2
    assert "s1" in merged_a1["sources"] and "s2" in merged_a1["sources"]

def test_asset_prioritization():
    assets = [
        {"asset_id": "a1", "risk_score": 40.0},
        {"asset_id": "a2", "risk_score": 90.0},
        {"asset_id": "a3", "risk_score": 10.0}
    ]
    ranked = AssetPrioritization.rank_assets(assets)
    assert ranked[0]["asset_id"] == "a2"
    assert ranked[0]["priority_rank"] == 1
    assert ranked[1]["asset_id"] == "a1"
    assert ranked[2]["asset_id"] == "a3"

def test_recommendation_generator():
    findings = [
        {"asset_id": "a1", "title": "TLS Weakness"},
        {"asset_id": "a2", "title": "TLS Weakness"},
        {"asset_id": "a3", "title": "Other Issue"}
    ]
    recs = RecommendationGenerator.generate_recommendations(findings)
    assert len(recs) == 1
    assert recs[0]["recommendation_id"] == "rec-tls"
    assert recs[0]["affected_assets"] == 2

def test_analytics_engine_profile():
    profile = AnalyticsEngine.build_asset_profile("a1", "1.1.1.1", 2, 5, 80.0)
    assert profile["asset_id"] == "a1"
    assert profile["ip"] == "1.1.1.1"
    assert profile["service_count"] == 2
    assert profile["risk_score"] == 80.0
