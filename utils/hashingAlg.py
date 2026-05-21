import hashlib
import os

def hash_new_password(password):
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000, dklen=64)
    return salt, dk

def verify_password(stored_salt, stored_hash, password_to_check):
    new_dk = hashlib.pbkdf2_hmac("sha256", password_to_check.encode(), stored_salt, 100000, dklen=64)
    return new_dk == stored_hash

def hash_password_no_salt(password):
    password_bytes = password.encode('utf-8')
    hash_object = hashlib.sha256(password_bytes)
    hashed_password = hash_object.hexdigest()
    
    return hashed_password
