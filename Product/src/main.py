from fastapi import FastAPI
from src.features.routes import product_router
from src.db.session import create_db_and_tables
from src.core.logging_middleware import LoggingMiddleware
from src.core.correlation_id_middleware import CorrelationIdMiddleware
from src.core.exception import BaseAppException
from fastapi.responses import JSONResponse
import logging
from src.core.logging_conf import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(CorrelationIdMiddleware)
app.add_middleware(LoggingMiddleware)

@app.exception_handler(Exception)
async def app_exception_handler(request, exc):
    logger.error("Application error: %s", exc.message)
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message}
    )

@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()


app.include_router(product_router, prefix="/api/v1", tags=["products"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, workers=4, loop="uvloop", http="h11")