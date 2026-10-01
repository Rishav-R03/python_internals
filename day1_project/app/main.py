from contextlib import asynccontextmanager
from api.v1.router import api_router
from core.resources import MockHttpClientPool
from fastapi import FastAPI,APIRouter
from settings import Environment,get_settings
from pydantic import ValidationError
import asyncio 
import httpx


@asynccontextmanager
async def lifespan(app:FastAPI):
    pool = MockHttpClientPool(base_url="https://api.internal-service.local")
    await pool.connect()
    app.state.http_pool = pool 
    yield 
    await app.state.http_pool.disconnect()

app = FastAPI(title="Production Scaffold API",lifespan=lifespan)
app.include_router(api_router,prefix="/api/v1")

router = APIRouter()

@app.get("/service/users")
async def get_user():
    await asyncio.sleep(1.0)
    return {"user_id":42,"name":"Rishav"} 

@app.get("/service/orders")
async def get_orders():
    await asyncio.sleep(1.0)
    return {"orders":["order_101","order_102"]}

@app.router.get("/dashboard") # main endpoint gathering data from services
async def get_dashboard():
    """Fetches user profile and orders concurrently using asyncio.gather()."""
    async with httpx.AsyncClient() as client:
        user_task = client.get("http://localhost:8001/service/users")
        orders_task = client.get("http://localhost:8001/service/orders")

        user_response,order_response = await asyncio.gather(user_task,orders_task)

        return {
            "status":"success",
            "data":{
                "user":user_response.json(),
                "orders":order_response.json(),
            },
        }

def run_demo():
    print("=== Test 1: First call to get_settings() ===")
    settings_1 = get_settings()
    print(f"App Name:     {settings_1.APP_NAME}")
    print(f"Environment:  {settings_1.ENV.value} (Type: {type(settings_1.ENV)})")
    print(f"Port:         {settings_1.PORT} (Type: {type(settings_1.PORT)})")
    print(f"Database Host:{settings_1.DATABASE_URL.host}")

    # Secrets are masked automatically when printed
    print(f"API Key Raw:  {settings_1.API_KEY}")
    print(f"API Key Ex:   {settings_1.API_KEY.get_secret_value()}")
    print()

    print("=== Test 2: Second call to get_settings() (LRU Cache Check) ===")
    # Notice that the "Reading environment..." print statement inside get_settings() does NOT run
    settings_2 = get_settings()
    print(f"Are instances identical in memory? {settings_1 is settings_2}")
    print()

    print("=== Test 3: Validation Guard Check (Simulating PROD with DEBUG=True) ===")
    try:
        from day1_project.app.settings import Settings

        # Attempting to boot with PROD + DEBUG=True triggers our custom validator
        invalid_prod_settings = Settings(
            ENV=Environment.PROD,
            DEBUG=True,
            DATABASE_URL="postgresql://user:pass@prod-db:5432/proddb",
            API_KEY="prod_secret_key",
        )
    except ValidationError as e:
        print("Successfully caught invalid production configuration:")
        print(e)


if __name__ == "__main__":
    import uvicorn
    run_demo()
    uvicorn.run("main:app",host="127.0.0.1",port=8001,reload=True)
    