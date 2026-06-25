import questionary
from apps.cli.ui import console
from operations.runbooks.doctor.doctor_engine import DoctorEngine
from operations.runbooks.doctor.repair_engine import RepairEngine


class DoctorMenu:
    @staticmethod
    def show():
        while True:
            console.print("\n=== ReconX Doctor ===", style="bold cyan")
            choice = questionary.select(
                "Select a Doctor Operation:",
                choices=[
                    "Scan System",
                    "Repair Missing Tools",
                    "Install Dependencies",
                    "Update Templates",
                    "Exit Doctor",
                ],
            ).ask()

            if choice == "Scan System":
                console.print("\n[*] Scanning environment...", style="yellow")
                report = DoctorEngine.scan()
                console.print(
                    f"Status: {report['status']}",
                    style="bold green" if report["status"] == "Healthy" else "bold red",
                )

                console.print("\nMissing Tools:")
                for t in report["missing_tools"]:
                    console.print(f"  - {t}", style="red")
                if not report["missing_tools"]:
                    console.print("  None (All tools installed!)", style="green")

            elif choice == "Repair Missing Tools":
                console.print("\n[*] Checking for missing tools to repair...")
                report = DoctorEngine.scan()
                missing = report["missing_tools"]
                if not missing:
                    console.print("[+] All tools are already installed.", style="green")
                else:
                    for t in missing:
                        res = RepairEngine.repair(t)
                        if res:
                            console.print(f"[+] Successfully repaired {t}", style="green")
                        else:
                            console.print(f"[-] Failed to repair {t}", style="red")

            elif choice == "Install Dependencies":
                console.print("\n[*] Not yet fully implemented. Run install.sh.", style="yellow")

            elif choice == "Update Templates":
                RepairEngine.update_templates()
                console.print("[+] Templates updated successfully.", style="green")

            elif choice == "Exit Doctor":
                break
