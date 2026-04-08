import asyncio
from collections import defaultdict


class StatusStreamService:
    def __init__(self):
        self.connections = defaultdict(list)

    async def subscribe(self, request_id: str):
        queue = asyncio.Queue()
        self.connections[request_id].append(queue)
        return queue

    def unsubscribe(self, request_id: str, queue: asyncio.Queue):
        if request_id in self.connections:
            self.connections[request_id] = [
                q for q in self.connections[request_id] if q != queue
            ]
            if not self.connections[request_id]:
                del self.connections[request_id]

    async def publish(self, request_id: str, data: dict):
        queues = self.connections.get(request_id, [])
        for queue in queues:
            await queue.put(data)


status_stream_service = StatusStreamService()