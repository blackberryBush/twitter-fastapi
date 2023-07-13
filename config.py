import os

import dotenv

dotenv.load_dotenv()


def not_found_message(env_name: str):
    return env_name + " not found. Please make sure it exists in environment variables."


HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(
    os.getenv("PORT", 7357)
)  # 7357 means TEST, so you have to explicitly mention port to run the app in production

DB_URL = os.getenv("DB_URL")
if DB_URL is None:
    raise OSError(not_found_message("Database URL"))

PAGINATION_MIN_LIMIT = os.getenv("PAGINATION_MIN_LIMIT", 1)
PAGINATION_DEFAULT_LIMIT = os.getenv("PAGINATION_DEFAULT_LIMIT", 20)
PAGINATION_MAX_LIMIT = os.getenv("PAGINATION_MAX_LIMIT", 50)

NAME_MAX_LENGTH = os.getenv("_NAME_MAX_LENGTH", 30)
VALUE_MAX_LENGTH = os.getenv("VALUE_MAX_LENGTH", 500)

SECRET_KEY = os.getenv("SECRET_KEY")
if SECRET_KEY is None:
    raise OSError(not_found_message("Secret Key"))
ALGORITHM = os.getenv("ALGORITHM")
if ALGORITHM is None:
    raise OSError(not_found_message("Algorithm"))

ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 10)
REFRESH_TOKEN_EXPIRE_DAYS = os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 10)
