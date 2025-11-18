from .database import SessionLocal


def get_pwd_context():
    # Use pbkdf2_sha256 to avoid native bcrypt issues
    from passlib.context import CryptContext

    return CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
