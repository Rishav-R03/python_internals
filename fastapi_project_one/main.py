from fastapi import FastAPI,Path,Query,Request
from pydantic import BaseModel, Field 
from typing import Optional
from contextlib import asynccontextmanager
from mock_pool import MockHttpClientPool

@asynccontextmanager
async def lifespan(app:FastAPI):
    """
    #1 Startup
    """
    print("App is starting...Initializing resources")

    #. Instantiate resources
    http_pool = MockHttpClientPool(base_url="https://api.external-service.com")
    # open connection
    await http_pool.connect()

    app.state.http_pool = http_pool
    yield # application runs while sitting at yield

    # 4. Gracefully close connections on server stop
    await app.state.http_pool.disconnect()
    print("App is shutting down...Cleaning up resources") 

app = FastAPI(title="FastAPI project one",lifespan=lifespan)

class User(BaseModel):
    name:str 
    age:int 

class Item(BaseModel):
    name: str = Field(...,example="Wireless Mouse")
    description: Optional[str] = Field(
        None,example="An ergonomic optional mouse"
    )
    price: float = Field(...,gt=0,example=29.99)
    tax:Optional[float] = Field(None,example=2.50)

# combined endpoint showing path, query, and body parameters
@app.put("/items/{item_id}")
async def update_item(
    item_id: int = Path(
        ...,ge=1,description="The ID of the item must be > 1"
    ),
    category: str = Query(
        ...,min_length=3,description="Filter category (Required)"
    ),
    notify: bool = Query(
        False,description="Send notification on update(Optional)"
    ),
    item: Item = None 
):
    """Updates an item using path,query and body inputs
    - **item_id**: Path Variable
    - **category**: Required Query Parameter
    - **notify**: Optional Query Parameter (defaults to False)
    - **item**: JSON Body payload parsed via Pydantic
    """
    total_price = item.price + (item.tax if item.tax else 0)
    return {
        "status":"success",
        "inputs_received" :{
            "path_variable":item_id,
            "query_param_category":category,
            "query_param_notifiy":notify,
            "body_payload":{
                "name":item.name,
                "description":item.description,
                "price":item.price,
                "tax":item.tax,
                "calculated_total": round(total_price,2),
            }
        }
    }


@app.get("/")
def home():
    return {"message":"Welcome to Home"}

@app.get("/about")
def about_route():
    return {"message":"This is about page"}

@app.get("/product/{product_id}")
def get_price(product_id:int,name:str = None,price:int = 0):
    return {
        "product_id":product_id,
        "name":f"{name}",
        "price":price,
    }

# posting data

@app.post("/products")
def create_product(name:str,price:int):
    return {
        "product_id":1,
        "produdct_name":name,
        "product_price": price
    }


# How Requests Access app.state
# Inside an endpoint handler, you can access app.state via the standard FastAPI Request object:

@app.get("/fetch")
async def fetch_external_data(request:Request):
    http_pool: MockHttpClientPool = request.app.state.http_pool
    result = await http_pool.fetch_data("users/123")
    return {"status":"success","result":result}