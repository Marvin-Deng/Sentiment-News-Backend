from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.article_router import router as article_router
from routes.stock_router import router as stock_router
from constants.env_consts import CLIENT_URL
from db import init_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[CLIENT_URL, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(article_router, prefix="/api/article")
app.include_router(stock_router, prefix="/api/stock")


@app.on_event("startup")
async def startup_event():
    await init_db()
