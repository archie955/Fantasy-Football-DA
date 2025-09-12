from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routers import get

app = FastAPI()
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "https://localhost",
    "https://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(get.router)

@app.get("/")
def root():
    return {"message": "home page"}