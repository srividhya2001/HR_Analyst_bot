import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """
    Application configuration settings.
    """
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DB_USER = "postgres"
    DB_PASSWORD = ""
    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_NAME = "postgres"


settings = Settings()