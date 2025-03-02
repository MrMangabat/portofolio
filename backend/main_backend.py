# # backend/main_backend.py

# import logging

# logging.basicConfig(
#     level=logging.INFO,  # Set the logging level to INFO
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# )

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from contextlib import asynccontextmanager
# from core_configuration.config import Config
# from core_configuration.database_connections import PostgresConnection
# from jobapplication_feature.api.routes import router as job_application_router

# config = Config()
# postgres_conn = PostgresConnection(config)

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     postgres_conn.create_tables()
#     yield

# app = FastAPI(lifespan=lifespan)

# # enable CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"], # http://localhost:5173
#     allow_credentials=False,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Print "Hello World" to the console when the application starts
# print("Hello World - Printed from main_backend.py!")

# ## testing, storing in memory
# words_list = ["dusk"]

# # Include the words router
# app.include_router(job_application_router)# Run table creation logic on startup


# @app.get("/")
# def read_root():
#     return{"Current words": words_list}

# # backend/main_backend.py
