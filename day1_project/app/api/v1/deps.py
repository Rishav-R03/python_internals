# dependency injection helper 
from app.core.resources import MockHttpClientPool
from fastapi import Request 

def get_http_pool(request:Request) -> MockHttpClientPool:
    """Dependency that extracts the initialized HTTP pool from app state."""
    return request.app.state.http_pool
