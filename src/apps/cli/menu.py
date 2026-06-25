import sys

import questionary

from apps.cli.doctor_menu import DoctorMenu
from apps.cli.project_menu import create_project, manage_projects, open_project
from apps.cli.ui import console, print_banner


def display_menu(session, config, launcher):
    while True:
        print_banner(session)

        console.print("═══════════════════════════════════════", style="dim")

        choice = questionary.select(
            "Select an option:",
            choices=[
                questionary.Choice(title="[1] Dashboard", value="1"),
                questionary.Choice(title="[2] Doctor", value="2"),
                questionary.Choice(title="[3] Projects", value="3"),
                questionary.Choice(title="[4] Settings", value="4"),
                questionary.Choice(title="[5] Exit", value="5"),
            ],
            qmark="?",
            instruction="(Use arrow keys)",
        ).ask()

        if choice == "1":
            launcher.start(project_name=session.current_project or "None")
            questionary.press_any_key_to_continue("Press any key to return to menu...").ask()
        elif choice == "2":
            DoctorMenu.show()
        elif choice == "3":
            # Sub-menu for projects
            p_choice = questionary.select(
                "Projects:", choices=["Open Project", "Create Project", "Manage Projects", "Back"]
            ).ask()
            if p_choice == "Open Project":
                open_project(session)
            elif p_choice == "Create Project":
                create_project(session)
            elif p_choice == "Manage Projects":
                manage_projects(session)
        elif choice == "4":
            while True:
                console.print("\n=== Enterprise Settings & Governance ===", style="bold cyan")
                s_choice = questionary.select(
                    "Settings:",
                    choices=[
                        "User Management",
                        "Team Management",
                        "Organizations",
                        "Roles & Permissions",
                        "Audit Logs",
                        "Activity Logs",
                        "Approval Requests",
                        "Plugin Manager",
                        "Marketplace",
                        "Connectors",
                        "Themes",
                        "SDK Tools",
                        "Distributed Nodes",
                        "Agent Manager",
                        "Cluster Manager",
                        "Node Health",
                        "Job Distribution",
                        "Scaling Policies",
                        "Back",
                    ],
                ).ask()

                if s_choice == "Back":
                    break
                else:
                    console.print(
                        f"[*] Accessing {s_choice} module via Dashboard APIs...", style="dim"
                    )
                    questionary.press_any_key_to_continue("Press any key to return...").ask()
        elif choice == "5":
            if questionary.confirm("Exit ReconX?").ask():
                if launcher.server_thread and launcher.server_thread.is_alive():
                    if questionary.confirm("Dashboard still running.\nClose dashboard?").ask():
                        pass
                console.print("Saving Session...")
                console.print("Closing ReconX...")
                console.print("Goodbye.")
                sys.exit(0)
