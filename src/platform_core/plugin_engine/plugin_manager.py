from core.legacy_core.plugin_db import Plugin, PluginPermission, SessionLocal
from platform_core.plugin_engine.plugin_loader import PluginLoader


class PluginManager:
    @staticmethod
    def sync_plugins():
        # Discovers plugins on disk and syncs them to the DB
        discovered = PluginLoader.discover_plugins()
        db = SessionLocal()

        for manifest in discovered:
            name = manifest.get("name")
            version = manifest.get("version")
            author = manifest.get("author")
            category = manifest.get("category", "Tool")

            p = db.query(Plugin).filter(Plugin.name == name).first()
            if not p:
                p = Plugin(
                    name=name, version=version, author=author, category=category, status="Installed"
                )
                db.add(p)
                db.commit()
                db.refresh(p)

                # Sync Permissions
                perms = manifest.get("permissions", [])
                for perm in perms:
                    db.add(PluginPermission(plugin_id=p.id, permission=perm))
                db.commit()

        db.close()

    @staticmethod
    def enable_plugin(plugin_id):
        db = SessionLocal()
        p = db.query(Plugin).filter(Plugin.id == plugin_id).first()
        if p:
            p.status = "Enabled"
            db.commit()
            # Here we would invoke PluginLoader.load_plugin
        db.close()

    @staticmethod
    def disable_plugin(plugin_id):
        db = SessionLocal()
        p = db.query(Plugin).filter(Plugin.id == plugin_id).first()
        if p:
            p.status = "Disabled"
            db.commit()
        db.close()
