from core.base_adapter import ToolAdapter


class SubfinderAdapter(ToolAdapter):
    def __init__(self, project_id, target):
        super().__init__("subfinder", project_id, target)


class NmapAdapter(ToolAdapter):
    def __init__(self, project_id, target):
        super().__init__("nmap", project_id, target)


class HttpxAdapter(ToolAdapter):
    def __init__(self, project_id, target):
        super().__init__("httpx", project_id, target)


class DnsxAdapter(ToolAdapter):
    def __init__(self, project_id, target):
        super().__init__("dnsx", project_id, target)


class NaabuAdapter(ToolAdapter):
    def __init__(self, project_id, target):
        super().__init__("naabu", project_id, target)


class NucleiAdapter(ToolAdapter):
    def __init__(self, project_id, target):
        super().__init__("nuclei", project_id, target)


class NiktoAdapter(ToolAdapter):
    def __init__(self, project_id, target):
        super().__init__("nikto", project_id, target)


class SslscanAdapter(ToolAdapter):
    def __init__(self, project_id, target):
        super().__init__("sslscan", project_id, target)


class TestsslAdapter(ToolAdapter):
    def __init__(self, project_id, target):
        super().__init__("testssl", project_id, target)


class FfufAdapter(ToolAdapter):
    def __init__(self, project_id, target):
        super().__init__("ffuf", project_id, target)


class DirsearchAdapter(ToolAdapter):
    def __init__(self, project_id, target):
        super().__init__("dirsearch", project_id, target)


class FeroxbusterAdapter(ToolAdapter):
    def __init__(self, project_id, target):
        super().__init__("feroxbuster", project_id, target)


class KatanaAdapter(ToolAdapter):
    def __init__(self, project_id, target):
        super().__init__("katana", project_id, target)


class LinkfinderAdapter(ToolAdapter):
    def __init__(self, project_id, target):
        super().__init__("linkfinder", project_id, target)


class SecretfinderAdapter(ToolAdapter):
    def __init__(self, project_id, target):
        super().__init__("secretfinder", project_id, target)


class JsfinderAdapter(ToolAdapter):
    def __init__(self, project_id, target):
        super().__init__("jsfinder", project_id, target)


class WaybackurlsAdapter(ToolAdapter):
    def __init__(self, project_id, target):
        super().__init__("waybackurls", project_id, target)


class GauAdapter(ToolAdapter):
    def __init__(self, project_id, target):
        super().__init__("gau", project_id, target)
