import asyncio 

class MockHttpClientPool:
    """Simulates an asynchronous HTTP client session or connection pool"""
    def __init__(self,base_url:str):
        self.base_url = base_url
        self.is_connected = False 

    async def connect(self):
        """Simulates establishing TCP connection / authentication."""
        print(f"[MOCK POOl] Connecting to service at {self.base_url}...")
        await asyncio.sleep(0.5) # simulate latency
        self.is_connected = True 
        print(f"[MOCK POOl] Connected successfully.")

    async def fetch_data(self,endpoint:str)->dict:
        """Simulates async http call over the open connection."""
        if not self.is_connected:
            raise RuntimeError(
                "Cannot fetch data: Resource Pool disconnected!"
            )
        return {
            "endpoint":f"{self.base_url}/{endpoint}",
            "status": 200,
            "data":"Mock Payload"
        }

    async def disconnect(self):
        """Simulates gracefully closing connection sockets"""
        print("[MOCK POOL] Closing active connection")
        await asyncio.sleep(.5)
        self.is_connected = False
        print("[MOCK POOl] Disconnected successfully.")
