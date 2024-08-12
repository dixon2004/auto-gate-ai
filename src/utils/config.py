from dotenv import load_dotenv
import os


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

MODEL_PATH = os.getenv("MODEL_PATH")

VIDEO_SOURCE = os.getenv("VIDEO_SOURCE")
if VIDEO_SOURCE.isdigit():
    VIDEO_SOURCE = int(VIDEO_SOURCE)

ACTION_OPTION = os.getenv("ACTION_OPTION")

ADMIN_PHONE_NUMBER = os.getenv("ADMIN_PHONE_NUMBER")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
