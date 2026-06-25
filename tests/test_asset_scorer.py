from recon.intelligence.asset_scorer import asset_scorer


def test_calculate_scores_production():
    """
    Test that a 'prod' asset receives a high business score.
    """
    asset = {"target": "prod-api.reconx.com", "is_public": True, "open_ports": [80, 443]}

    scores = asset_scorer.calculate_scores(asset)

    assert scores["business_score"] == 80
    assert scores["exposure_score"] == 60  # 50 + (2 * 5)
    assert scores["risk_score"] == int((80 * 0.4) + (60 * 0.6))
    assert scores["confidence_score"] == 100


def test_calculate_scores_staging_private():
    """
    Test that a private 'staging' asset receives a lower business and exposure score.
    """
    asset = {"target": "staging.internal.reconx.local", "is_public": False, "open_ports": []}

    scores = asset_scorer.calculate_scores(asset)

    assert scores["business_score"] == 30
    assert scores["exposure_score"] == 0
    assert scores["risk_score"] == int((30 * 0.4) + (0 * 0.6))
    assert scores["confidence_score"] == 100


def test_calculate_scores_no_keywords():
    """
    Test an asset with no identifiable keywords.
    """
    asset = {"target": "unknown-host.com", "is_public": True, "open_ports": [80]}

    scores = asset_scorer.calculate_scores(asset)

    assert scores["business_score"] == 0
    assert scores["exposure_score"] == 55  # 50 + (1 * 5)
    assert scores["risk_score"] == int((0 * 0.4) + (55 * 0.6))
    assert scores["confidence_score"] == 100
