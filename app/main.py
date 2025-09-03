from fastapi import FastAPI, Query, Body, Path
import uvicorn

from hotels import router as hotel_router

app = FastAPI()
app.include_router(hotel_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)