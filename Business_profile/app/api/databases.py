import os
import psycopg2
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db_connection():
    try:
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            connect_timeout=10
        )
        logger.info("✅ Connected successfully to PostgreSQL database")
        return connection
    except psycopg2.Error as e:
        logger.error("❌ ERROR: Could not connect to PostgreSQL.")
        logger.error(e)
        return None
