from core.screenshot_db import SessionLocal, OCRResult

class OCREngine:
    @staticmethod
    def extract_text(asset_id, image_path):
        # Simulating Tesseract OCR engine extraction
        # Real logic: pytesseract.image_to_string(Image.open(image_path))
        extracted_text = "Welcome Administrator. Please enter your credentials to access the internal portal."
        
        db = SessionLocal()
        res = OCRResult(asset_id=asset_id, text=extracted_text)
        db.add(res)
        db.commit()
        db.close()
        return extracted_text
