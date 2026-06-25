import ipaddress


class TargetExpander:
    """Expands CIDR subnets and IP ranges into distinct targets."""

    @staticmethod
    def expand(target_str: str) -> list[str]:
        target_str = target_str.strip()

        # Handle CIDR
        if "/" in target_str:
            try:
                network = ipaddress.ip_network(target_str, strict=False)
                return [str(ip) for ip in network.hosts()]
            except ValueError:
                pass

        # Handle simple range 192.168.1.1-10
        if "-" in target_str:
            base, range_end = target_str.split("-")
            try:
                ipaddress.ip_address(base)
                prefix = ".".join(base.split(".")[:-1])
                start_last_octet = int(base.split(".")[-1])
                end_last_octet = int(range_end)

                expanded = []
                for octet in range(start_last_octet, end_last_octet + 1):
                    expanded.append(f"{prefix}.{octet}")
                return expanded
            except ValueError:
                pass

        # Return as-is if no expansion matched
        return [target_str]
