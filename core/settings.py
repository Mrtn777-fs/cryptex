"""Settings management for Cryptex"""
import json
import os
from typing import Dict, Any

SETTINGS_FILE = "data/settings.json"

DEFAULT_SETTINGS = {
    "theme": "dark_red",
    "auto_save": True,
    "auto_save_interval": 30,  # seconds
    "show_welcome": True,
    "font_size": 14,
    "window_geometry": None,
    "backup_on_exit": False,
    "session_timeout": 0,  # 0 = no timeout
    "show_note_count": True,
    "confirm_delete": True,
    "recent_files": []
}

class Settings:
    def __init__(self):
        self.settings = self.load_settings()
    
    def load_settings(self) -> Dict[str, Any]:
        """Load settings from file or return defaults"""
        if not os.path.exists(SETTINGS_FILE):
            return DEFAULT_SETTINGS.copy()
        
        try:
            with open(SETTINGS_FILE, 'r') as f:
                loaded = json.load(f)
                # Merge with defaults to ensure all keys exist
                settings = DEFAULT_SETTINGS.copy()
                settings.update(loaded)
                return settings
        except Exception:
            return DEFAULT_SETTINGS.copy()
    
    def save_settings(self):
        """Save current settings to file"""
        os.makedirs("data", exist_ok=True)
        try:
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"Failed to save settings: {e}")
    
    def get(self, key: str, default=None):
        """Get a setting value"""
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set a setting value"""
        self.settings[key] = value
        self.save_settings()
    
    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        self.settings = DEFAULT_SETTINGS.copy()
        self.save_settings()

# Global settings instance
settings = Settings()