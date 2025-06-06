from fastapi import FastAPI

app = FastAPI()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, workers=4, loop="uvloop", http="h11")