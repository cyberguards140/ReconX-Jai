from core.plugin_db import SessionLocal, ThemeRegistry

class ThemeEngine:
    @staticmethod
    def set_active_theme(theme_name):
        db = SessionLocal()
        # Disable all
        db.query(ThemeRegistry).update({ThemeRegistry.is_active: False})
        
        t = db.query(ThemeRegistry).filter(ThemeRegistry.theme_name == theme_name).first()
        if t:
            t.is_active = True
        else:
            t = ThemeRegistry(theme_name=theme_name, is_active=True)
            db.add(t)
            
        db.commit()
        db.close()
        return True
