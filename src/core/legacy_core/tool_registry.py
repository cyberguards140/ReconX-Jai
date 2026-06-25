import logging

from core.legacy_core.registry_db import Category, SessionLocal, Tool, ToolArgument, ToolDependency


class ToolRegistry:
    @staticmethod
    def get_categories():
        db = SessionLocal()
        categories = db.query(Category).order_by(Category.order).all()
        result = [c.name for c in categories]
        db.close()
        return result

    @staticmethod
    def get_tools():
        db = SessionLocal()
        tools = db.query(Tool).all()
        result = [
            {
                "id": t.id,
                "name": t.name,
                "category": t.category_id,
                "status": "installed" if t.enabled else "disabled",
            }
            for t in tools
        ]
        db.close()
        return result

    @staticmethod
    def get_tool(tool_id):
        db = SessionLocal()
        t = db.query(Tool).filter(Tool.id == tool_id).first()
        if not t:
            db.close()
            return None

        args = db.query(ToolArgument).filter(ToolArgument.tool_id == tool_id).all()
        deps = db.query(ToolDependency).filter(ToolDependency.tool_id == tool_id).all()

        result = {
            "id": t.id,
            "name": t.name,
            "description": t.description,
            "category": t.category_id,
            "version": t.version,
            "binary": t.binary,
            "enabled": t.enabled,
            "execution": {"type": t.execution_type},
            "output": {"live_terminal": t.live_terminal},
            "tags": t.tags,
            "arguments": [
                {"flag": a.flag, "type": a.type, "default": a.default_value} for a in args
            ],
            "dependencies": [{"type": d.dep_type, "name": d.name} for d in deps],
        }
        db.close()
        return result

    @staticmethod
    def get_tool_arguments(tool_id):
        db = SessionLocal()
        args = db.query(ToolArgument).filter(ToolArgument.tool_id == tool_id).all()
        result = [{"flag": a.flag, "type": a.type, "default": a.default_value} for a in args]
        db.close()
        return result

    @staticmethod
    def get_tool_status(tool_id):
        db = SessionLocal()
        t = db.query(Tool).filter(Tool.id == tool_id).first()
        db.close()
        if t:
            return "installed" if t.enabled else "disabled"
        return "missing"

    @staticmethod
    def set_tool_status(tool_id, enabled):
        db = SessionLocal()
        t = db.query(Tool).filter(Tool.id == tool_id).first()
        if t:
            t.enabled = enabled
            db.commit()

            # Log action
            logger = logging.getLogger("registry")
            logger.info(f"Tool {tool_id} {'Enabled' if enabled else 'Disabled'}")
        db.close()
