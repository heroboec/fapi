from pathlib import Path
from fastapi import FastAPI
import uvicorn
import sys
sys.path.append(str(Path(__file__).parent.parent))
from src.api.hotels import router as hotel_router
from src.api.auth import router as user_router

app = FastAPI()
app.include_router(user_router)
app.include_router(hotel_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
