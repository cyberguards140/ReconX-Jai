from collections import defaultdict
from datetime import datetime


class TimelineEngine:
    def __init__(self):
        # target -> timeline of events
        self.ledgers: dict[str, list[dict]] = defaultdict(list)

    def log_change(self, target: str, event_type: str, details: str):
        """Records a chronological ledger entry."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event_type,
            "details": details,
        }
        self.ledgers[target].append(entry)
        print(f"[TIMELINE] {target}: {event_type} - {details}")

    def get_timeline(self, target: str) -> list[dict]:
        return self.ledgers.get(target, [])

    def get_all_ledgers(self) -> dict[str, list[dict]]:
        return dict(self.ledgers)


timeline_engine = TimelineEngine()
