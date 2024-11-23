"""
main.py

Contains app initialization, routes and setup
"""
from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routers import batch

app = FastAPI()

app.include_router(batch.router)


@app.on_event("startup")
def on_startup():
    """
    Create database and tables
    """
    create_db_and_tables()
