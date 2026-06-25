from reconx.modules.analytics.recommendations import RecommendationGenerator

class RecommendationEngineService:
    @staticmethod
    def generate(findings: list[dict]) -> list[dict]:
        return RecommendationGenerator.generate_recommendations(findings)
