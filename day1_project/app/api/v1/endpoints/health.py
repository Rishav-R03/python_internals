from app.api.v1.deps import get_http_pool
from app.core.resources import MockHttpClientPool
from fastapi import APIRouter,Depends

router = APIRouter()

@router.get("/health")
async def health_check(
    pool:MockHttpClientPool = Depends(get_http_pool),
):
    """Health Check endpoint that uses our pooled connection."""
    result = await pool.fetch_data("status")
    return {
        "status":"healthy",
        "pool_status":"connected" if pool.is_connected else "disconnected",
        "pool_response":result,
    }

