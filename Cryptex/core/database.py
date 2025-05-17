import os
import json
import shutil
from core.encryptor import encrypt, decrypt

DB_FILE = "data/vault.enc"

def load_data(pin):
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "rb") as f:
        encrypted = f.read()
    try:
        decrypted = decrypt(pin, encrypted)
        return json.loads(decrypted)
    except:
        return {}

def save_data(pin, title, content):
    data = load_data(pin)
    data[title] = content
    with open(DB_FILE, "wb") as f:
        f.write(encrypt(pin, json.dumps(data)))

def delete_note(pin, title):
    data = load_data(pin)
    if title in data:
        del data[title]
        with open(DB_FILE, "wb") as f:
            f.write(encrypt(pin, json.dumps(data)))

def export_vault(path):
    shutil.copy(DB_FILE, path)

def import_vault(path):
    shutil.copy(path, DB_FILE)