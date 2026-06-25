import questionary

from apps.cli.ui import console


class ProfileEngine:
    @staticmethod
    def seed_profiles():
        pass

    @staticmethod
    def get_profiles():
        return []


class Project:
    status = "Active"
    name = "dummy"
    description = "dummy"
    id = "dummy-id"


class SessionLocal:
    def query(self, *args):
        return self

    def filter(self, *args):
        return self

    def all(self):
        return []

    def close(self):
        pass


class ProjectManager:
    @staticmethod
    def create_project(*args):
        return "dummy-id"

    @staticmethod
    def add_target(*args):
        pass


def manage_projects(session):
    console.print("\n=== Project Workspace Manager ===", style="bold cyan")

    choice = questionary.select(
        "Select an option:",
        choices=[
            "Create Project",
            "Web Enumeration",
            "Cloud Intelligence",
            "Campaign Management",
            "Reporting",
            "Automation",
            "Asset Intelligence",
            "Analytics Center",
            "Close Project",
            "Existing Projects",
            "Campaigns",
            "Profiles",
            "Workflows",
            "Reports",
            "Import",
            "Archive",
            "Back",
        ],
    ).ask()

    if choice == "Create Project":
        create_project(session)
    elif choice == "Analytics Center":
        manage_analytics(session)
    elif choice == "Close Project":
        open_project(session)
    elif choice == "Open Project":
        open_project(session)
    elif choice == "Existing Projects":
        list_existing_projects()
    elif choice == "Campaigns":
        console.print("[*] Loading Campaign Engine...")
    elif choice == "Profiles":
        ProfileEngine.seed_profiles()
        console.print("\n=== Scan Profiles ===")
        for p in ProfileEngine.get_profiles():
            console.print(f"- {p['name']} ({len(p['tools'])} tools)")
    elif choice == "Workflows":
        manage_workflows(session)
    elif choice == "Asset Intelligence":
        manage_asset_intelligence(session)
    elif choice == "Reports":
        manage_reports(session)
    elif choice == "Import":
        console.print("[*] Importing Project...")
    elif choice == "Archive":
        console.print("[*] Archiving Project...")


def create_project(session):
    console.print("\n=== Create Project ===")
    name = questionary.text("Project Name:").ask()
    desc = questionary.text("Description:").ask()
    client = questionary.text("Client:").ask()
    targets = questionary.text("Targets (comma-separated):").ask()

    project_id = ProjectManager.create_project(name, desc, client, [])
    if project_id:
        console.print(f"\n[+] Project '{name}' created successfully.", style="bold green")
        session.set_project(name, project_id)
        if targets:
            for t in targets.split(","):
                ProjectManager.add_target(project_id, "domain", t.strip())
    else:
        console.print("\n[-] Project already exists.", style="bold red")


def open_project(session):
    db = SessionLocal()
    projects = db.query(Project).filter(Project.status != "Archived").all()
    db.close()

    if not projects:
        console.print("\n[-] No active projects found.", style="bold yellow")
        return

    choices = [p.name for p in projects] + ["Cancel"]
    choice = questionary.select("Select a project:", choices=choices).ask()

    if choice and choice != "Cancel":
        project = next((p for p in projects if p.name == choice), None)
        session.set_project(project.name, project.id)
        console.print(f"\n[+] Opened Project: {project.name}", style="bold green")


def list_existing_projects():
    db = SessionLocal()
    projects = db.query(Project).all()
    db.close()

    if not projects:
        console.print("\n[-] No projects found.", style="bold yellow")
        return

    console.print("\n=== Existing Projects ===")
    for p in projects:
        console.print(f"[{p.status}] {p.name} - {p.description}")


def manage_reports(session):
    if not session.project_id:
        console.print("[-] Open a project first.", style="bold red")
        return

    console.print("\n=== Report Center ===", style="bold cyan")
    choice = questionary.select(
        "Generate:",
        choices=[
            "Executive Report",
            "Technical Report",
            "Vulnerability Report",
            "Cloud Report",
            "Campaign Report",
            "Evidence Package",
            "Export Center",
            "Back",
        ],
    ).ask()

    from reporting.evidence_packager import EvidencePackager

    from reporting.report_engine import ReportEngine

    if choice == "Evidence Package":
        EvidencePackager.create_package(session.project_id, session.current_project)
    elif choice in [
        "Executive Report",
        "Technical Report",
        "Vulnerability Report",
        "Cloud Report",
        "Campaign Report",
    ]:
        ReportEngine.generate_report(
            session.project_id, session.current_project, choice.split(" ")[0].lower()
        )
    elif choice == "Export Center":
        console.print("[*] Exporting project data...")


def manage_workflows(session):
    if not session.project_id:
        console.print("[-] Open a project first.", style="bold red")
        return

    console.print("\n=== Automation & Workflows ===", style="bold cyan")
    choice = questionary.select(
        "Automation:",
        choices=[
            "Create Workflow",
            "Existing Workflows",
            "Schedule Workflow",
            "Workflow History",
            "Alerts",
            "Back",
        ],
    ).ask()

    from core.automation.alert_manager import AlertManager
    from core.automation.scheduler import SchedulerEngine
    from core.automation.workflow_engine import WorkflowEngine

    if choice == "Create Workflow":
        name = questionary.text("Workflow Name:").ask()
        steps = questionary.text("Tools (comma-separated):").ask().split(",")
        WorkflowEngine.create_workflow(session.project_id, name, [s.strip() for s in steps])
        console.print(f"[+] Workflow {name} created.")
    elif choice == "Existing Workflows":
        wfs = WorkflowEngine.get_workflows(session.project_id)
        for w in wfs:
            console.print(f"- {w['name']} ({len(w['steps'])} tools)")
    elif choice == "Schedule Workflow":
        wfs = WorkflowEngine.get_workflows(session.project_id)
        if not wfs:
            console.print("[-] No workflows exist.")
            return
        w_choice = questionary.select("Select Workflow:", choices=[w["name"] for w in wfs]).ask()
        freq = questionary.select("Frequency:", choices=["daily", "weekly", "monthly"]).ask()
        time_str = questionary.text("Time (HH:MM):").ask()

        w_id = next(w["id"] for w in wfs if w["name"] == w_choice)
        SchedulerEngine.schedule_job(w_id, freq, time_str)
        console.print(f"[+] Workflow {w_choice} scheduled.")
    elif choice == "Alerts":
        alerts = AlertManager.get_unread(session.project_id)
        if not alerts:
            console.print("[+] No unread alerts.")
        for a in alerts:
            console.print(f"[{a['severity'].upper()}] {a['type']}: {a['message']}")


def manage_intelligence(session):
    if not session.project_id:
        console.print("[-] Open a project first.", style="bold red")
        return

    console.print("\n=== Asset Intelligence Center ===", style="bold cyan")
    choice = questionary.select(
        "Intelligence Operations:",
        choices=[
            "Asset Explorer",
            "Relationship Map",
            "Advanced Search",
            "Risk Center",
            "Timeline",
            "Screenshot Center",
            "Login Portals",
            "Admin Portals",
            "Visual Findings",
            "OCR Search",
            "Preview Center",
            "Threat Center",
            "CVE Center",
            "IOC Explorer",
            "Reputation Center",
            "Exposure Monitor",
            "ASN Explorer",
            "Passive DNS",
            "Back",
        ],
    ).ask()

    from core.intelligence.search_engine import SearchEngine
    from core.screenshots.screenshot_manager import ScreenshotManager

    from core.legacy_core.intelligence_db import SessionLocal, UniversalAsset

    if choice == "Screenshot Center":
        console.print("\n=== Screenshot Center ===")
        url = questionary.text("URL to capture:").ask()
        if url:
            ScreenshotManager.process_asset(session.current_project, "temp-id", url)
    elif choice == "Asset Explorer":
        db = SessionLocal()
        assets = (
            db.query(UniversalAsset).filter(UniversalAsset.project_id == session.project_id).all()
        )
        console.print(f"Total Assets: {len(assets)}")
        for a in assets[:10]:
            console.print(f"- [{a.asset_type}] {a.value} (Risk: {a.risk_score})")
        db.close()
    elif choice == "Advanced Search":
        q = questionary.text("Search Query:").ask()
        res = SearchEngine.search(q)
        console.print(f"Found {len(res)} results.")
        for r in res:
            console.print(f"- [{r['type']}] {r['value']} (Risk: {r['risk']})")
    elif choice == "CVE Center":
        from core.legacy_core.threat_db import CVEData
        from core.legacy_core.threat_db import SessionLocal as ThreatSession

        db = ThreatSession()
        cves = db.query(CVEData).all()
        console.print(f"Total CVEs Correlated: {len(cves)}")
        for c in cves[:10]:
            console.print(f"- {c.cve} (Severity: {c.severity})")
        db.close()
    elif choice in [
        "Relationship Map",
        "Risk Center",
        "Timeline",
        "Threat Center",
        "IOC Explorer",
        "Reputation Center",
        "Exposure Monitor",
        "ASN Explorer",
        "Passive DNS",
    ]:
        console.print(f"[*] Accessing {choice} framework via Dashboard APIs...", style="dim")


def manage_analytics(session):
    while True:
        console.print(f"\n[bold magenta]Analytics Center[/] - {session.current_project}")
        choice = questionary.select(
            "Select Analytics Module:",
            choices=[
                "Executive Intelligence",
                "Trends",
                "Risk Analytics",
                "Exposure Analytics",
                "Forecasts",
                "Historical Data",
                "KPIs",
                "Back",
            ],
        ).ask()

        if choice == "Back":
            break
        else:
            console.print(
                f"[*] Accessing {choice} module via Dashboard Analytics APIs...", style="dim"
            )
            questionary.press_any_key_to_continue("Press any key to return...").ask()


def manage_asset_intelligence(session):
    while True:
        console.print(
            f"\n[bold green]Asset Intelligence & Graph Explorer[/] - {session.current_project}"
        )
        choice = questionary.select(
            "Select Graph Module:",
            choices=[
                "Knowledge Graph",
                "Relationship Explorer",
                "Attack Paths",
                "Infrastructure Map",
                "Investigations",
                "Graph Analytics",
                "Exposure Center",
                "Risk Center",
                "Security Posture",
                "Remediation Center",
                "Ownership",
                "SLA Tracking",
                "Executive Risk",
                "Back",
            ],
        ).ask()

        if choice == "Back":
            break
        else:
            console.print(f"[*] Exploring {choice} correlations via Graph APIs...", style="dim")
            questionary.press_any_key_to_continue("Press any key to return...").ask()


def manage_campaigns(session):
    while True:
        console.print("\n[bold cyan]Campaign Center[/]")
        choice = questionary.select(
            "Select Campaign Module:",
            choices=[
                "Active Campaigns",
                "Engagements",
                "Scope Manager",
                "Tasks",
                "Milestones",
                "Evidence",
                "Operations Center",
                "Analytics",
                "Back",
            ],
        ).ask()

        if choice == "Back":
            break
        else:
            console.print(f"[*] Accessing {choice} workspace via Campaign APIs...", style="dim")
            questionary.press_any_key_to_continue("Press any key to return...").ask()


def manage_cases(session):
    while True:
        console.print("\n[bold magenta]Case Center & Investigation Ops[/]")
        choice = questionary.select(
            "Select Case Module:",
            choices=[
                "Open Cases",
                "Investigations",
                "Evidence",
                "Artifacts",
                "Reviews",
                "Timeline",
                "Analytics",
                "Back",
            ],
        ).ask()

        if choice == "Back":
            break
        else:
            console.print(f"[*] Loading {choice} module via Case APIs...", style="dim")
            questionary.press_any_key_to_continue("Press any key to return...").ask()
