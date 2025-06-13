from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from db import async_session
import asyncio

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    mongo_client = AsyncIOMotorClient("mongodb://localhost:27017")
    mongo_db = mongo_client["your_read_db"]

    async def projection_loop():
        while True:
            async with async_session() as session:
                await process_projection_queue(session, mongo_db)
            await asyncio.sleep(30)

    asyncio.create_task(projection_loop())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, workers=4, loop="uvloop", http="h11")