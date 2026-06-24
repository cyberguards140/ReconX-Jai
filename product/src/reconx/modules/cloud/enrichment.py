class CloudEnricher:
    """Heuristics to determine cloud/container target types."""
    
    @staticmethod
    def is_aws_account(target: str) -> bool:
        return target.startswith("arn:aws:") or target == "aws"

    @staticmethod
    def is_kubeconfig(target: str) -> bool:
        return target == "kubeconfig" or target.startswith("k8s:")

    @staticmethod
    def is_container_image(target: str) -> bool:
        return ":" in target and not target.startswith("arn:aws:") and not target.startswith("k8s:")
