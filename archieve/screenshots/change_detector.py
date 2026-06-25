import random
from core.screenshot_db import SessionLocal, VisualChange

class ChangeDetector:
    @staticmethod
    def detect_changes(asset_id, current_screenshot_id, previous_screenshot_id):
        # Simulate an image hash / SSIM comparison (Structural Similarity Index)
        # Real logic: cv2.absdiff / skimage.metrics.structural_similarity
        change_score = round(random.uniform(0.0, 100.0), 2)
        
        db = SessionLocal()
        vc = VisualChange(asset_id=asset_id, change_score=change_score, prev_screenshot_id=previous_screenshot_id)
        db.add(vc)
        db.commit()
        db.close()
        return change_score
