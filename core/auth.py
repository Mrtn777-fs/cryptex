import os
from argon2 import PasswordHasher

hasher = PasswordHasher()

PIN_FILE = "data/pin.hash"

def set_pin(pin):
    os.makedirs("data", exist_ok=True)
    hashed = hasher.hash(pin)
    with open(PIN_FILE, "w") as f:
        f.write(hashed)

def pin_exists():
    """Check if a PIN has been set"""
    return os.path.exists(PIN_FILE)

def check_pin(pin):
    try:
        with open(PIN_FILE, "r") as f:
            stored = f.read()
        hasher.verify(stored, pin)
        return True
    except:
        return False