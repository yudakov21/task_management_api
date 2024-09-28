from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME= os.environ.get("DB_NAME")
DB_HOST= os.environ.get("DB_HOST")
DB_PASS= os.environ.get("DB_PASS")
DB_PORT= os.environ.get("DB_PORT")
DB_USER= os.environ.get("DB_USER")