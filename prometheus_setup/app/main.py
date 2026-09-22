from fastapi import FastAPI
from fastapi.responses import Response 
from prometheus_client import generate_latest,CONTENT_TYPE_LATEST

from .middleware import PrometheusMiddleware
from .routes import routes as task_router 

app = FastAPI(title="Fast + Prometheus")

app.add_middleware(PrometheusMiddleware)
app.include_router(task_router)

@app.get("/metrics",include_in_schema=False)
def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

@app.get("/")
def root(): 
    return {"message":"Welcome to the demo"}
