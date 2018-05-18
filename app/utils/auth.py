import bcrypt


def hash_password(password):
    """
    Encode the password for storage to the database.
    The database password field is defined as String, for which reason
    under Python 3, the generated hash needs to be decoded to 'utf-8', the
    default for this app.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(password, hashed):
    """
    Check if the password sent at login matches the database password.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
