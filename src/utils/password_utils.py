from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def truncate_for_bcrypt(password: str) -> str:
    pw_bytes = password.encode("utf-8")[:72]
    return pw_bytes.decode("utf-8", "ignore") 

def hash_password(password: str):
    return pwd_context.hash(truncate_for_bcrypt(password=password))

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(truncate_for_bcrypt(plain_password), hashed_password)


