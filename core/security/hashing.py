from passlib.context import CryptContext


context = CryptContext(schemes=['bcrypt'])


def get_hash_password(raw_password: str, /) -> str:
    return context.hash(raw_password)


def verify_password(raw_password: str, hash_password: str, /) -> bool:
    return context.verify(raw_password, hash_password)