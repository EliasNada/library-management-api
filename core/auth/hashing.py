import bcrypt


def verify_hash(plain_secret: str, hashed_secret: str):
    secret_byte_enc = plain_secret.encode('utf-8')
    hashed_secret = hashed_secret.encode('utf-8')
    return bcrypt.checkpw(password=secret_byte_enc, hashed_password=hashed_secret)

def get_hash(secret: str):
    secret_bytes = secret.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(password=secret_bytes, salt=salt)
    return hash.decode('utf-8')