# backend/api_gateway/src/main_system_trigger.py

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from routes import router
from config.api_gateway_settings import APIGatewaySettings

# Load settings directly from Pydantic-powered config
settings = APIGatewaySettings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Placeholder for any startup/init logic (e.g., DB warm-up, service ping)
    yield

# Instantiate FastAPI app
app = FastAPI(lifespan=lifespan)
app.add_middleware(         # # Enable CORS using validated env values
    CORSMiddleware,
    allow_origins=[
        "http://localhost:9000", # MinIO
        "http://localhost:5173", # frontend dev server
        # "http://localhost:8080", # api gateway
        "http://localhost:8010"  # cover letter service
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("\n🚀 API_GATEWAY is running!\n")

# Attach main router
app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "🔥 THIS IS THE API GATEWAY"}
