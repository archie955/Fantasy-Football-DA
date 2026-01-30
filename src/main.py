from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .backend.routers import get, build, trade, update, login

app = FastAPI()
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "https://localhost",
    "https://localhost:8080",
    "http://localhost:5173",
    "http://localhost:5173/",
    "http://localhost:5173/home",
    "https://localhost:5173/team"
]

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(get.router)
app.include_router(build.router)
app.include_router(trade.router)
app.include_router(update.router)
app.include_router(login.router)

@app.get("/")
def root():
    return {"message": "home page"}