import subprocess
import logging
from src.config.config_low_level import PostgressConnection
from src.data_models.postgres_models import Base

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def run_reset_schema():
    logging.info("Running reset_schema.sh to reset the database schema...")
    result = subprocess.run(["sh", "./reset_schema.sh"], capture_output=True, text=True)
    if result.returncode == 0:
        logging.info("Schema reset completed successfully.")
    else:
        logging.error(f"Schema reset failed:
{result.stderr}")
        raise RuntimeError("Schema reset failed. Check the logs above.")

def ensure_tables_exist():
    logging.info("Ensuring all tables exist in the database (just in case schema reset failed).")
    PostgressConnection.Base.metadata.create_all(PostgressConnection.engine)
    logging.info("Table check/creation completed.")

if __name__ == "__main__":
    try:
        run_reset_schema()
        ensure_tables_exist()
        logging.info("Startup process completed successfully.")
    except Exception as e:
        logging.error(f"Startup process failed: {e}")
        exit(1)
