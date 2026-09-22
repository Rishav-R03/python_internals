# app/core/resources.py
import asyncio


class MockHttpClientPool:
    """Simulates an asynchronous client pool or database connection pool."""

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.is_connected = False

    async def connect(self):
        print(f"🔌 [MOCK POOL] Connecting to service at {self.base_url}...")
        await asyncio.sleep(0.3)  # Simulate startup connection latency
        self.is_connected = True
        print("✅ [MOCK POOL] Connection pool ready.")

    async def fetch_data(self, endpoint: str) -> dict:
        if not self.is_connected:
            raise RuntimeError("Pool is not connected!")
        return {
            "endpoint": f"{self.base_url}/{endpoint}",
            "status": "ok",
            "data": "Payload retrieved via pooled connection",
        }

    async def disconnect(self):
        print("🔌 [MOCK POOL] Draining and closing connection pool...")
        await asyncio.sleep(0.2)  # Simulate graceful shutdown delay
        self.is_connected = False
        print("🛑 [MOCK POOL] Pool closed cleanly.")