from core.screenshot_db import SessionLocal, LoginPage

class LoginDetector:
    @staticmethod
    def detect(asset_id, ocr_text, url):
        # Determine if it's a login page using OCR text and URL heuristics
        is_login = False
        login_type = "Basic"
        
        keywords = ["password", "login", "sign in", "credentials", "sso"]
        if any(k in ocr_text.lower() for k in keywords) or "login" in url.lower() or "admin" in url.lower():
            is_login = True
            if "sso" in ocr_text.lower() or "oauth" in ocr_text.lower():
                login_type = "SSO"
        
        if is_login:
            db = SessionLocal()
            lp = LoginPage(asset_id=asset_id, type=login_type)
            db.add(lp)
            db.commit()
            db.close()
            return login_type
        return None
