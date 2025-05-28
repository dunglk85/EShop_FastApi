from fastapi import FastAPI
from src.features.createproduct import router as create_product_router
from src.db.session import create_db_and_tables
from src.core.logging_middleware import LoggingMiddleware

app = FastAPI()
app.add_middleware(LoggingMiddleware)
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(create_product_router, prefix="/api/v1", tags=["products"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)