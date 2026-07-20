import os 
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Settings:
    PROJECT_NAME: str = "BAM System"
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "mysql+pymysql://root@localhost:3306/BAM_System"
    )

    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "BAM_SECRET_2026"
    )

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)

settings = Settings()