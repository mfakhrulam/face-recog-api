import os
from dotenv import load_dotenv

load_dotenv()

STATIC_DIR = os.environ.get("STATIC_DIR") or 'static'
POSTGRES_USER = os.environ.get("POSTGRES_USER") or 'postgres'
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD") or 'password'
POSTGRES_DB = os.environ.get("POSTGRES_DB") or 'db_face_recog'
HOST = os.environ.get("HOST") or 'db'
POSTGRES_PORT = os.environ.get("POSTGRES_PORT") or '5432'
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
