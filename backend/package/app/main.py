"""
Fast API entrypoint
This file controls the entry point for the API, Build the fastapi object here and register the different routers to it
"""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware #(midend connection stuff)

from app.routers import equipment, auth, work_order, hospital, technician, service_report


FRONTEND_ORIGIN = os.environ.get("FRONTEND_ORIGIN", "http://localhost:5173")


app = FastAPI(
    title = "Medflow Command Center",
    description = "Equipment Management API for Medflow",
    version="0.1.0"
)

#CORS goes here
app.add_middleware(
    CORSMiddleware,
    #The endpoint for our frontend
    allow_origins=[FRONTEND_ORIGIN],
    #This allows us to pass an Auth header (JWT)
    allow_credentials=True,
    #This allows all methods and headers through
    allow_methods=["*"],
    allow_headers=["*"],
)



#Include routers in API
app.include_router(equipment.router)
app.include_router(auth.router)
app.include_router(work_order.router)
app.include_router(hospital.router)
app.include_router(technician.router)
app.include_router(service_report.router)

#Sample health endpoint to validate connection
@app.get("/health", tags = ['health'])
async def health_check() -> dict[str, str]:
    return {"status" : "ok"}
