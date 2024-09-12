import os
from dotenv import load_dotenv
from analytics.db import init_db

load_dotenv()

os.environ['RUN_TIMEZONE_CHECK'] = '0'

if __name__ == "__main__":
    print("Initializing database...")
    init_db()