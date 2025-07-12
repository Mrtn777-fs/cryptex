"""
Cryptex - Modern Secure Note Manager
A beautiful, encrypted note-taking application with glassmorphism design.
"""
import sys
import os
from gui.login import LoginWindow
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

def setup_application():
    """Setup application with modern styling"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Cryptex")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("Cryptex")
    app.setOrganizationDomain("cryptex.local")
    
    # Use native styling as base
    app.setStyle('Fusion')
    
    return app

def main():
    """Main application entry point"""
    try:
        # Create data directory if it doesn't exist
        os.makedirs("data", exist_ok=True)
        
        # Setup application
        app = setup_application()
        
        # Create and show login window
        login_window = LoginWindow()
        login_window.show()
        
        # Run application
        return app.exec()
        
    except Exception as e:
        print(f"Application error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())