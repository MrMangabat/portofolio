# backend/services/service_cover_letter/startup.py
import os
import socket
import subprocess
import logging
from dotenv import load_dotenv
# from src.data_models.postgres_models import Base

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

'''
Pre-boot process:
✅ Reset database schema (runs reset_schema.sh)
✅ Ensure all tables exist (failsafe in case reset fails)
✅ Dynamically resolve MinIO IP (in case network assigns a new one)
✅ Save resolved MinIO IP into a fresh env file (used by MinioConnection later)
'''

# def resolve_minio_ip() -> str:
#     try:
#         minio_ip = socket.gethostbyname("cover_letter_minio")
#         logging.info(f"✅ Resolved cover_letter_minio to {minio_ip}")
#         return minio_ip
#     except socket.gaierror as e:
#         logging.error(f"❌ Failed to resolve cover_letter_minio: {e}")
#         raise

def write_resolved_env(minio_ip: str) -> None:
    with open("/app/service_cover_letter/src/resolved_env.env", "w") as file:
        file.write(f"MINIO_IP={minio_ip}\n")
    logging.info("✅ resolved_env.env written successfully")

def run_reset_schema() -> None:
    logging.info("Running reset_schema.sh to reset the database schema...")
    result = subprocess.run(["sh", "./reset_schema.sh"], capture_output=True, text=True)
    if result.returncode == 0:
        logging.info("✅ Schema reset completed successfully.")
    else:
        logging.error(f"❌ Schema reset failed:\n{result.stderr}")
        raise RuntimeError("Schema reset failed. Check the logs above.")

def pre_startup() -> None:
    try:
        # minio_ip = resolve_minio_ip()
        # write_resolved_env(minio_ip)
        run_reset_schema()
        logging.info("✅ Pre-startup process completed successfully.")
    except Exception as e:
        logging.error(f"❌ Pre-startup process failed: {e}")
        raise