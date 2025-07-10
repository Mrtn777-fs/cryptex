import sys
import os
from gui.login import LoginWindow
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from core.settings import settings

def setup_application():
    """Setup application properties"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Cryptex")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("Cryptex")
    app.setOrganizationDomain("cryptex.local")
    
    # Enable high DPI scaling
    app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    
    return app

def main():
    """Main application entry point"""
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Setup application
    app = setup_application()
    
    # Create and show login window
    login_window = LoginWindow()
    login_window.show()
    
    # Run application
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())