import logging
import uuid
from typing import Any

from sqlalchemy import select

from data.database.models import SOARWorkflowTemplate
from data.database.session import async_session_factory

logger = logging.getLogger(__name__)

# Built-in Playbooks
BUILTIN_PLAYBOOKS = [
    {
        "name": "SOC_Incident_Triage",
        "description": "Automatically triages an incoming SOC incident by enriching IP addresses and querying Threat Intelligence.",
        "version": 1,
        "definition": {
            "trigger": "IncidentCreated",
            "tasks": [
                {"name": "Extract Indicators", "action": "extract_iocs"},
                {"name": "Query Threat Intel", "action": "query_ti"},
                {"name": "Update Severity", "action": "update_incident_severity"},
            ],
        },
    },
    {
        "name": "ASM_Vulnerability_Scan",
        "description": "Trigger a targeted vulnerability scan when a new exposed port is discovered.",
        "version": 1,
        "definition": {
            "trigger": "PortDiscovered",
            "tasks": [
                {"name": "Run Nmap", "action": "scan_port"},
                {"name": "Run Nuclei", "action": "scan_vulns"},
                {"name": "Create Alert", "action": "create_vulnerability_alert"},
            ],
        },
    },
]


class PlaybookEngine:
    """
    Manages the installation and synchronization of built-in and custom security playbooks.
    """

    async def sync_builtin_playbooks(self):
        """
        Ensures all built-in playbooks are present in the SOAR database.
        """
        async with async_session_factory() as session:
            for pb in BUILTIN_PLAYBOOKS:
                result = await session.execute(
                    select(SOARWorkflowTemplate).filter(SOARWorkflowTemplate.name == pb["name"])
                )
                existing = result.scalars().first()

                if not existing:
                    logger.info(f"Installing built-in playbook: {pb['name']}")
                    template = SOARWorkflowTemplate(
                        id=str(uuid.uuid4()),
                        name=pb["name"],
                        description=pb["description"],
                        version=pb["version"],
                        definition_json=pb["definition"],
                    )
                    session.add(template)
                else:
                    # Update definition if needed
                    existing.definition_json = pb["definition"]
                    existing.description = pb["description"]

            await session.commit()
            logger.info("Built-in playbooks synchronized.")

    async def get_all_playbooks(self) -> list[dict[str, Any]]:
        async with async_session_factory() as session:
            result = await session.execute(select(SOARWorkflowTemplate))
            templates = result.scalars().all()
            return [
                {
                    "id": t.id,
                    "name": t.name,
                    "description": t.description,
                    "version": t.version,
                    "definition": t.definition_json,
                }
                for t in templates
            ]
