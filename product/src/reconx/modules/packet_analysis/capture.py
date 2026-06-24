import os

class CaptureSource:
    """Helper to verify if a target is a live interface or a PCAP file."""
    
    @staticmethod
    def is_pcap(target: str) -> bool:
        return target.endswith(".pcap") or target.endswith(".pcapng")

    @staticmethod
    def is_interface(target: str) -> bool:
        return target in ["eth0", "wlan0", "tun0"] or not CaptureSource.is_pcap(target)
