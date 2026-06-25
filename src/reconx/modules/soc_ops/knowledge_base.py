class KnowledgeBaseEngine:
    """
    Archives completed investigations to preserve organizational memory.
    """
    def __init__(self):
        self.articles = []

    def archive_case(self, case_id: str, summary: str, lessons_learned: str):
        self.articles.append({
            "case_id": case_id,
            "summary": summary,
            "lessons_learned": lessons_learned
        })
