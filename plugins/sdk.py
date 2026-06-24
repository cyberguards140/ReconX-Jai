class ReconXPlugin:
    def __init__(self, context=None):
        self.context = context
        self.name = self.__class__.__name__

    def register_tool(self, tool_name, executable, args):
        print(f"[{self.name}] Registering Custom Tool: {tool_name}")
        # In a real system, this pushes to core/tool_registry.py

    def on_load(self):
        pass

    def on_unload(self):
        pass

# Decorator for hooking into core events
def on_event(event_type):
    def decorator(func):
        func._is_event_hook = True
        func._hook_event_type = event_type
        return func
    return decorator
