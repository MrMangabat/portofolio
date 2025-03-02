# backend/services/service_cover_letter/src/api_cover_letter_main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from src.config.config_low_level import PostgressConnection
from service_cover_letter.src.routes import router as cover_letter_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    db_generator = PostgressConnection.get_db()
    session: Session = next(db_generator)

    try:
        PostgressConnection.Base.metadata.create_all(PostgressConnection.engine)

        if session.execute(text("SELECT COUNT(*) FROM corrections")).scalar() == 0:
            print("⚙️ Prepopulating corrections table from SQL file...")
            with open("src/data_models/sql_models/words_setences_skills.sql", "r", encoding="utf-8") as file:
                sql_content = file.read()

            for statement in sql_content.split(";"):
                if statement.strip():
                    session.execute(text(statement))
            session.commit()
            print("Corrections table prepopulated.")
        else:
            print("Corrections table already has data — skipping prepopulation.")

        yield

    finally:
        session.close()

app = FastAPI(lifespan=lifespan)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # http://localhost:5173 if needed later
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the cover letter routes
app.include_router(cover_letter_router)
