class RelationshipScoring:
    @staticmethod
    def evaluate_confidence(evidence_type):
        scores = {
            "DNS": 100.0,
            "Certificate": 95.0,
            "Shared_IP": 60.0,
            "Technology": 80.0
        }
        return scores.get(evidence_type, 50.0)
