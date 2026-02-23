import mysql.connector
from src.config import DB_CONFIG

def get_connection():
    """Establish and return a MySQL database connection."""
    return mysql.connector.connect(**DB_CONFIG)
