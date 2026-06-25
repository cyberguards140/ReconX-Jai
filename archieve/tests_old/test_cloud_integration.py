import pytest
from reconx.plugins.adapters.scoutsuite_adapter import ScoutsuiteAdapter
from reconx.plugins.adapters.trivy_adapter import TrivyAdapter
from reconx.plugins.adapters.dockerbench_adapter import DockerbenchAdapter
from reconx.plugins.adapters.kubectl_adapter import KubectlAdapter
from reconx.modules.cloud.orchestrator import CloudOrchestrator
from reconx.modules.cloud.enrichment import CloudEnricher
from reconx.modules.cloud.correlation import CloudCorrelation

@pytest.mark.asyncio
async def test_scoutsuite_adapter_command():
    adapter = ScoutsuiteAdapter()
    cmd = await adapter.build_command("aws")
    assert "scout" in cmd
    assert "aws" in cmd
    assert "--no-browser" in cmd

@pytest.mark.asyncio
async def test_trivy_adapter_command():
    adapter = TrivyAdapter()
    cmd = await adapter.build_command("nginx:latest")
    assert "trivy" in cmd
    assert "image" in cmd
    assert "nginx:latest" in cmd
    assert "json" in cmd

@pytest.mark.asyncio
async def test_dockerbench_adapter_command():
    adapter = DockerbenchAdapter()
    cmd = await adapter.build_command("local")
    assert "docker-bench-security" in cmd
    assert "-c" in cmd
    assert "container_images" in cmd

@pytest.mark.asyncio
async def test_kubectl_adapter_command():
    adapter = KubectlAdapter()
    cmd = await adapter.build_command("kubeconfig")
    assert "kubectl" in cmd
    assert "get" in cmd
    assert "all" in cmd
    assert "--all-namespaces" in cmd

@pytest.mark.asyncio
async def test_cloud_orchestrator_aws():
    result = await CloudOrchestrator.run_cloud_analysis("arn:aws:iam::123456789012:root")
    assert result["status"] == "scheduled"
    assert result["target_type"] == "aws"
    assert "scoutsuite" in result["tasks"]

@pytest.mark.asyncio
async def test_cloud_orchestrator_k8s():
    result = await CloudOrchestrator.run_cloud_analysis("kubeconfig")
    assert result["status"] == "scheduled"
    assert result["target_type"] == "kubernetes"
    assert "kubectl" in result["tasks"]

@pytest.mark.asyncio
async def test_cloud_orchestrator_container():
    result = await CloudOrchestrator.run_cloud_analysis("redis:alpine")
    assert result["status"] == "scheduled"
    assert result["target_type"] == "container"
    assert "trivy" in result["tasks"]
    assert "dockerbench" in result["tasks"]

def test_cloud_enricher_heuristics():
    assert CloudEnricher.is_aws_account("arn:aws:iam::123456789012:user/admin") is True
    assert CloudEnricher.is_aws_account("aws") is True
    assert CloudEnricher.is_kubeconfig("k8s:prod-cluster") is True
    assert CloudEnricher.is_kubeconfig("kubeconfig") is True
    assert CloudEnricher.is_container_image("ubuntu:20.04") is True
    assert CloudEnricher.is_container_image("arn:aws:ecr") is False # ECR ARN is an AWS target

def test_cloud_correlation():
    mapped = CloudCorrelation.map_cloud_ip_to_asset("i-0abcd1234efgh5678", "54.12.34.56")
    assert mapped["source"] == "i-0abcd1234efgh5678"
    assert mapped["target"] == "54.12.34.56"
    assert mapped["type"] == "resolves_to"
