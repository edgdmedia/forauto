import os

from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")
WEBSITE_NAME = os.getenv("WEBSITE_NAME")
DEBUG = os.getenv("DEBUG")
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
SECRET_KEY = os.getenv("SECRET_KEY")
REFRESH_TOKEN_EXPIRE_TIME = os.getenv("REFRESH_TOKEN_EXPIRE_TIME")
ACCESS_TOKEN_EXPIRE_TIME = os.getenv("ACCESS_TOKEN_EXPIRE_TIME")
REFRESH_KEY = os.getenv("REFRESH_KEY")
API_URL = "/api/v1"
