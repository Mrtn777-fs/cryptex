import os
import json
import shutil
from core.encryptor import encrypt, decrypt

DB_FILE = "data/vault.enc"

def load_data(pin):
    """Load encrypted data from vault"""
    try:
        if not os.path.exists(DB_FILE):
            return {}
        
        with open(DB_FILE, "rb") as f:
            encrypted = f.read()
        
        if not encrypted:
            return {}
        
        decrypted = decrypt(pin, encrypted)
        return json.loads(decrypted)
    except Exception as e:
        print(f"Error loading data: {e}")
        return {}

def save_data(pin, title, content):
    """Save encrypted data to vault"""
    try:
        data = load_data(pin)
        data[title] = content
        
        os.makedirs("data", exist_ok=True)
        
        with open(DB_FILE, "wb") as f:
            f.write(encrypt(pin, json.dumps(data)))
        
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False

def delete_note(pin, title):
    """Delete a note from the vault"""
    try:
        data = load_data(pin)
        if title in data:
            del data[title]
            
            os.makedirs("data", exist_ok=True)
            
            with open(DB_FILE, "wb") as f:
                f.write(encrypt(pin, json.dumps(data)))
        
        return True
    except Exception as e:
        print(f"Error deleting note: {e}")
        return False

def export_vault(path):
    """Export vault to specified path"""
    try:
        if os.path.exists(DB_FILE):
            shutil.copy(DB_FILE, path)
            return True
        return False
    except Exception as e:
        print(f"Error exporting vault: {e}")
        return False

def import_vault(path):
    """Import vault from specified path"""
    try:
        if os.path.exists(path):
            os.makedirs("data", exist_ok=True)
            shutil.copy(path, DB_FILE)
            return True
        return False
    except Exception as e:
        print(f"Error importing vault: {e}")
        return False