"""
Fast API entrypoint
This file controls the entry point for the API, Build the fastapi object here and register the different routers to it
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware #CORS is for later (midend connection stuff)

from app.routers import equipment, auth

app = FastAPI(
    title = "Medflow Command Center",
    description = "Equipment Management API for Medflow",
    version="0.1.0"
)

#CORS goes here




#Include routers in API
app.include_router(equipment.router)
app.include_router(auth.router)

#Sample health endpoint to validate connection
@app.get("/health", tags = ['health'])
async def health_check() -> dict[str, str]:
    return {"status" : "ok"}
