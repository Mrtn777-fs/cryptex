import os
from argon2 import PasswordHasher

PIN_FILE = "data/pin.hash"

def set_pin(pin):
    """Set a new PIN"""
    try:
        os.makedirs("data", exist_ok=True)
        hasher = PasswordHasher()
        hashed = hasher.hash(pin)
        with open(PIN_FILE, "w") as f:
            f.write(hashed)
        return True
    except Exception as e:
        print(f"Error setting PIN: {e}")
        return False

def pin_exists():
    """Check if a PIN has been set"""
    return os.path.exists(PIN_FILE)

def check_pin(pin):
    """Check if the provided PIN is correct"""
    try:
        if not pin_exists():
            return False
        
        with open(PIN_FILE, "r") as f:
            stored = f.read().strip()
        
        hasher = PasswordHasher()
        hasher.verify(stored, pin)
        return True
    except Exception as e:
        print(f"Error checking PIN: {e}")
        return False