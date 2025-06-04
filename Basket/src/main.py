from fastapi import FastAPI
from src.routes.endpoints import router
from src.core.logging_middleware import LoggingMiddleware
from src.core.correlation_id_middleware import CorrelationIdMiddleware
from fastapi.responses import JSONResponse
import logging
from src.core.logging_conf import setup_logging
from src.wait_for_kafka import wait_for_kafka
from fastapi import HTTPException
from src.config import message_bus

setup_logging()
logger = logging.getLogger(__name__)
app = FastAPI()
app.add_middleware(CorrelationIdMiddleware)
app.add_middleware(LoggingMiddleware)

@app.exception_handler(Exception)
async def app_exception_handler(request, exc):
    logger.error("Application error: %s", str(exc))
    # If it's an HTTPException, use its status_code
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message}
    )

@app.on_event("startup")
async def startup_event():
    await wait_for_kafka()
    await message_bus.start()

@app.on_event("shutdown")
async def shutdown_event():
    await message_bus.stop()

app.include_router(router, prefix="/api/v1", tags=["basket"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, workers=4, loop="uvloop", http="h11")