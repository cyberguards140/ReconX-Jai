from unittest.mock import patch

from ai.agents.swarm import ai_swarm


@patch("ai.agents.swarm.ReconAgent.analyze")
@patch("ai.agents.swarm.CorrelationAgent.correlate")
@patch("ai.agents.swarm.ReportingAgent.generate_report")
def test_ai_swarm_investigation_pipeline(mock_generate, mock_correlate, mock_analyze):
    """
    Test that the AI Swarm passes data correctly between the Agents.
    """
    # Set up mocks
    mock_analyze.return_value = "recon_results"
    mock_correlate.return_value = "correlated_results"
    mock_generate.return_value = "final_report"

    # Execute Swarm
    target = "api.reconx.com"
    result = ai_swarm.run_investigation(target)

    # Assert sequence was executed correctly
    mock_analyze.assert_called_once_with(target)
    mock_correlate.assert_called_once_with("recon_results")
    mock_generate.assert_called_once_with("correlated_results")

    # Assert final output
    assert result == "final_report"
