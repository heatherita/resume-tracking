import os

DATABASE_URL = os.getenv("DATABASE_URL", "")
APP_NAME=os.getenv("APP_NAME", "FastAPI App")