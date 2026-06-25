from rich.console import Console
from rich.text import Text

console = Console()

BANNER = """██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗██╗  ██╗
██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║╚██╗██╔╝
██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║ ╚███╔╝
██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║ ██╔██╗
██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║██╔╝ ██╗
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝"""


def print_banner(session):
    console.clear()
    console.print(Text(BANNER, style="bold cyan"))
    console.print()
    console.print("ReconX Attack Surface Management Platform", style="bold white")
    console.print()
    console.print("Version : 1.0.0")
    console.print("Status  : Ready", style="green")
    console.print("Mode    : Local First")
    console.print()
    project_str = session.current_project if session.current_project else "None"
    console.print(f"Current Project : [bold yellow]{project_str}[/bold yellow]")
    console.print()
