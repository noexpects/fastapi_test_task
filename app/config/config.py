from functools import lru_cache
from dotenv import load_dotenv
from os import environ


class Settings:
    def __init__(self):
        load_dotenv()
        # DB_Settings
        self.db_user = environ.get("POSTGRES_USER")
        self.db_pass = environ.get("POSTGRES_PASSWORD")
        self.db_host = environ.get("DB_HOST")
        self.db_name = environ.get("POSTGRES_DB")
        self.test_db_name = environ.get("TEST_DB_NAME")
        # Hash settings
        self.salt_len = int(environ.get("SALT_LEN"))
        self.hash_algoritm = environ.get("HASH_ALGORITM")
        self.iter_number = int(environ.get("ITERATIONS_NUM"))


@lru_cache(maxsize=128)
def get_settings():
    return Settings()
