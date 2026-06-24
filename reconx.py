#!/usr/bin/env python3
import os
import sys

script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)
sys.path.insert(0, script_dir)

from core.session import SessionManager
from core.config import ConfigLoader
from dashboard.backend.dashboard_manager import DashboardManager
from cli.menu import display_menu
from core.registry_seeder import seed_registry
from doctor.doctor_engine import DoctorEngine
from cli.ui import console

def quick_health_check():
    try:
        report = DoctorEngine.scan()
        if report['status'] in ['Warning', 'Critical']:
            console.print("\n[!] Warning:", style="bold yellow")
            if "nuclei" in report['missing_tools']:
                console.print("Nuclei Missing", style="bold red")
            console.print(f"{len(report['missing_tools'])} tools missing.", style="yellow")
            console.print("Run: ReconX Doctor -> Repair Missing Tools\n", style="bold cyan")
    except Exception as e:
        pass

def main():
    quick_health_check()
    seed_registry()
    config = ConfigLoader()
    session = SessionManager()
    
    port = config.get('dashboard_port', 3000)
    auto_open = config.get('auto_open_browser', True)
    
    launcher = DashboardManager(port=port, auto_open=auto_open)
    
    try:
        display_menu(session, config, launcher)
    except KeyboardInterrupt:
        print("\nSaving Session...")
        print("Closing ReconX...")
        print("Goodbye.")
        sys.exit(0)

if __name__ == "__main__":
    main()
