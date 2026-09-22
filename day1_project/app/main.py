from contextlib import asynccontextmanager
from app.api.v1.router import api_router
from app.core.resources import MockHttpClientPool
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app:FastAPI):
    pool = MockHttpClientPool(base_url="https://api.internal-service.local")
    await pool.connect()
    app.state.http_pool = pool 
    yield 
    await app.state.http_pool.disconnect()

app = FastAPI(title="Production Scaffold API",lifespan=lifespan)
app.include_router(api_router,prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app",host="127.0.0.1",port=8000,reload=True)
    