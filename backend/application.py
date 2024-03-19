#main file of flask application
# import psycopg2
## ----------------- Imports root path ----------------- ##
import sys
import os
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))  # Adjust the path to include the root directory

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from backend.databases.postgres_database.create_database import SessionLocal
from backend.crud import get_working_experiences, get_education

# create and initialize a new FastAPI app
app = FastAPI()

# enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Dependcy
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# define your routes and endpoints using FastAPI decorators
@app.get("/get-working-experiences")
def read_working_experiences(db: Session = Depends(get_db)):
    return get_working_experiences(db)

@app.get("/get-education")
def read_education(db: Session = Depends(get_db)):
    return get_education(db)