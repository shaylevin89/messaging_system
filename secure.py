from werkzeug.security import generate_password_hash, check_password_hash


def hash_generate(password):
    hashed_password = generate_password_hash(password, 'sha256')
    return hashed_password


def login_check(db_password, auth_password):
    if check_password_hash(db_password, auth_password):
        return True
    return False
