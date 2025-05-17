from cryptography.fernet import Fernet
import base64
import hashlib

def key_from_pin(pin):
    return base64.urlsafe_b64encode(hashlib.sha256(pin.encode()).digest())

def encrypt(pin, data):
    f = Fernet(key_from_pin(pin))
    return f.encrypt(data.encode())

def decrypt(pin, token):
    f = Fernet(key_from_pin(pin))
    return f.decrypt(token).decode()