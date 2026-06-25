from screenshots.ocr_engine import OCREngine
from screenshots.login_detector import LoginDetector
from screenshots.fingerprinting import FingerprintingEngine
from core.screenshot_db import SessionLocal, VisualFinding
from dashboard.backend.websocket import broadcast

class VisualIntelligence:
    @staticmethod
    def process_image(asset_id, url, image_path):
        print(f"[*] Processing visual intelligence for {url}...")
        
        # 1. Extract Text
        ocr_text = OCREngine.extract_text(asset_id, image_path)
        
        # 2. Fingerprint Technologies
        tech = FingerprintingEngine.fingerprint(asset_id, ocr_text, url)
        
        # 3. Detect Login Pages
        login_type = LoginDetector.detect(asset_id, ocr_text, url)
        
        # 4. Generate Visual Findings
        db = SessionLocal()
        finding_type = None
        if login_type and "admin" in url.lower():
            finding_type = "Exposed Admin Panel"
        elif tech != "Unknown" and "default" in ocr_text.lower():
            finding_type = f"Default {tech} Dashboard"
            
        if finding_type:
            vf = VisualFinding(asset_id=asset_id, finding_type=finding_type)
            db.add(vf)
            db.commit()
            print(f"[!] Visual Finding: {finding_type}")
            
        db.close()
        
        # Broadcast Results
        broadcast({
            "type": "screenshot_processed",
            "asset_id": asset_id,
            "url": url,
            "technology": tech,
            "login_detected": bool(login_type),
            "finding": finding_type
        })
        
        return {
            "ocr_length": len(ocr_text),
            "technology": tech,
            "login_type": login_type,
            "finding": finding_type
        }
