from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

class Hash:
    def verify(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)