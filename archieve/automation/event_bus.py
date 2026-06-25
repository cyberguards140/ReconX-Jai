class EventBus:
    _subscribers = []

    @classmethod
    def subscribe(cls, callback):
        cls._subscribers.append(callback)

    @classmethod
    def publish(cls, event_type, payload):
        event = {"event": event_type, **payload}
        for sub in cls._subscribers:
            try:
                sub(event)
            except Exception as e:
                print(f"[-] EventBus subscriber failed: {e}")
