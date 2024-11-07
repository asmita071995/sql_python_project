# config.py
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine

# Load environment variables from the .env file
load_dotenv()

# Store variables as constants
username = os.getenv("username")
password = os.getenv("password")
host = os.getenv("host")
database = os.getenv("database")
