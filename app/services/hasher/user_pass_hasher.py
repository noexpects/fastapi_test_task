import os
import hashlib
from app.config import config

settings = config.get_settings()


class PassHasher:
    def __init__(self):
        self.salt_len = settings.salt_len
        self.hash_algoritm = settings.hash_algoritm
        self.iter_number = settings.iter_number

    async def generate_hash(self, password):
        salt = os.urandom(self.salt_len)
        key = hashlib.pbkdf2_hmac(self.hash_algoritm, password.encode('utf-8'), salt, self.iter_number)
        hashed_password = salt+key
        return hashed_password.hex()
