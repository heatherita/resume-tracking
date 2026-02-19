from config.settings import APP_NAME
from config.logging_config import setup_logger
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from database import Base, engine, get_db



logger = setup_logger()
logger.info("Backend started")


# settings = get_settings()

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title=APP_NAME)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from routers import admin, format

# --- App ---

app.include_router(admin.router, prefix="/api")         # e.g., /api/qa
app.include_router(format.router, prefix="/api")         # e.g., /api/q


