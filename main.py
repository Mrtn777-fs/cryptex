"""
Cryptex - Simple, Secure Note Manager
Clean, functional, and actually works.
"""
import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

def main():
    """Main application entry point"""
    try:
        # Create data directory
        os.makedirs("data", exist_ok=True)
        
        # Create application
        app = QApplication(sys.argv)
        app.setApplicationName("Cryptex")
        app.setApplicationVersion("2.0")
        
        # Import and create login window
        from gui.login import LoginWindow
        login_window = LoginWindow()
        login_window.show()
        
        # Run application
        return app.exec()
        
    except Exception as e:
        print(f"Application error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())