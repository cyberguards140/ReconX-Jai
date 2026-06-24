class EventHookEngine:
    _hooks = {}

    @classmethod
    def register_hook(cls, event_type, callback):
        if event_type not in cls._hooks:
            cls._hooks[event_type] = []
        cls._hooks[event_type].append(callback)

    @classmethod
    def dispatch(cls, event_type, *args, **kwargs):
        if event_type in cls._hooks:
            for callback in cls._hooks[event_type]:
                try:
                    callback(*args, **kwargs)
                except Exception as e:
                    print(f"[EventHookEngine] Error executing hook for {event_type}: {e}")
