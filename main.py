"""
Cryptex - Modern Secure Note Manager
Beautiful, encrypted, and actually works perfectly.
"""
import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

def main():
    """Main application entry point"""
    try:
        # Create data directory
        os.makedirs("data", exist_ok=True)
        
        # Create application
        app = QApplication(sys.argv)
        app.setApplicationName("Cryptex")
        app.setApplicationVersion("3.0")
        
        # Set application font
        font = QFont("Segoe UI", 10)
        app.setFont(font)
        
        # Import and create login window
        from gui.login import LoginWindow
        login_window = LoginWindow()
        login_window.show()
        
        # Run application
        return app.exec()
        
    except Exception as e:
        print(f"Application error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())