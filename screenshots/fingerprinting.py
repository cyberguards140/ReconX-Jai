from core.screenshot_db import SessionLocal, Fingerprint

class FingerprintingEngine:
    @staticmethod
    def fingerprint(asset_id, ocr_text, url):
        # Simulating visual tech identification (like Wappalyzer via DOM + images)
        detected_tech = None
        text_lower = ocr_text.lower()
        
        if "wp-admin" in url or "wordpress" in text_lower:
            detected_tech = "WordPress"
        elif "jenkins dashboard" in text_lower:
            detected_tech = "Jenkins"
        elif "grafana" in text_lower:
            detected_tech = "Grafana"
        elif "aws console" in text_lower:
            detected_tech = "AWS Console"
            
        if detected_tech:
            db = SessionLocal()
            fp = Fingerprint(asset_id=asset_id, technology=detected_tech)
            db.add(fp)
            db.commit()
            db.close()
            return detected_tech
        return "Unknown"
