import os
from dotenv import load_dotenv

load_dotenv()

STATIC_DIR = os.environ.get("STATIC_DIR")
DATABASE_URL = os.environ.get("DATABASE_URL")
