#backend/api_gateway/src/main_system_trigger.py

import logging
import os
# logging.basicConfig(
#     level=logging.INFO,  # Set the logging level to INFO
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# )

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from routes import router  # Ensure absolute import
from config.dependencies import get_api_gateway_settings


settings = get_api_gateway_settings()
print(f"\n[INFO] ALLOWED_ORIGINS loaded: {settings.top.get_allowed_origins_list}\n")  # Log it to confirm

@asynccontextmanager
async def lifespan(app: FastAPI):
    # data.create_tables()
    yield

app = FastAPI(lifespan=lifespan)

# enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.top.get_allowed_origins_list(), # http://localhost:5173
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Print "Hello World" to the console when the application starts
print("\nmain_system_trigger.py!\n")

## testing, storing in memory
words_list = ["test"]

# Include the words router
app.include_router(router)

@app.get("/")
def read_root():
    return {"message:": "API_GATEWAY is running"}