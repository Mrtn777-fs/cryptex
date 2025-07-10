import os
import json
from argon2 import PasswordHasher

hasher = PasswordHasher()

PIN_FILE = "data/pin.hash"
AUTH_CONFIG_FILE = "data/auth_config.json"

def get_auth_config():
    """Get authentication configuration"""
    if not os.path.exists(AUTH_CONFIG_FILE):
        return {"pin_length": 4, "max_attempts": 5, "lockout_time": 300}
    
    try:
        with open(AUTH_CONFIG_FILE, "r") as f:
            return json.load(f)
    except:
        return {"pin_length": 4, "max_attempts": 5, "lockout_time": 300}

def save_auth_config(config):
    """Save authentication configuration"""
    os.makedirs("data", exist_ok=True)
    with open(AUTH_CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

def set_pin(pin):
    os.makedirs("data", exist_ok=True)
    hashed = hasher.hash(pin)
    with open(PIN_FILE, "w") as f:
        f.write(hashed)

def change_pin(old_pin, new_pin):
    """Change the PIN after verifying the old one"""
    if not check_pin(old_pin):
        return False
    set_pin(new_pin)
    return True

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