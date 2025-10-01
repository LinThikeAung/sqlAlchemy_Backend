from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import os
from .database import engine, Base, SessionLocal
from . import schemas, crud
from fastapi.middleware.cors import CORSMiddleware
from .routers import users


app_title = os.getenv("APP_NAME", "Async SQLAlchemy CRUD API")  # default if not set

app = FastAPI(title=app_title)

origins = [
    "http://localhost:5173",  # React dev server
    "http://127.0.0.1:5173",  # in case React uses 127.0.0.1
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # or ["*"] to allow all origins (not recommended for production)
    allow_credentials=True,
    allow_methods=["*"],         # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],         # Authorization, Content-Type, etc.
)

# Create tables async on startup
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(users.router)
