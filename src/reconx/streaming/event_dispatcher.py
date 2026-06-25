class EventDispatcher:
    def __init__(self):
        self.subscribers = {}

    async def subscribe(self, channel, queue):
        if channel not in self.subscribers:
            self.subscribers[channel] = set()
        self.subscribers[channel].add(queue)

    async def unsubscribe(self, channel, queue):
        if channel in self.subscribers:
            self.subscribers[channel].discard(queue)

    async def dispatch(self, channel, event):
        if channel in self.subscribers:
            for queue in self.subscribers[channel]:
                await queue.put(event)


event_dispatcher = EventDispatcher()
