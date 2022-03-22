from passlib.hash import pbkdf2_sha256


# Password hasher
def hash_password(password: str):
    return pbkdf2_sha256.hash(password)


# Verify hashed password
def verify_password(password: str, hashed_password: str):
    '''Returns true if passwords match.'''
    return pbkdf2_sha256.verify(password, hashed_password)
