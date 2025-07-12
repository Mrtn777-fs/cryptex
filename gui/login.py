"""Simple, clean login window that actually works"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QFrame, QApplication)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import os
from core.auth import check_pin, set_pin, pin_exists

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cryptex - Secure Vault")
        self.setFixedSize(400, 500)
        
        # Simple dark theme
        self.setStyleSheet("""
            QWidget {
                background-color: #1a1a1a;
                color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QFrame {
                background-color: #2a2a2a;
                border: 1px solid #00CFFF;
                border-radius: 16px;
                padding: 30px;
            }
            QLabel {
                color: #00CFFF;
                font-weight: bold;
            }
            QLineEdit {
                background-color: #333333;
                border: 2px solid #00CFFF;
                border-radius: 8px;
                padding: 15px;
                font-size: 18px;
                color: white;
            }
            QLineEdit:focus {
                border-color: #66D9FF;
            }
            QPushButton {
                background-color: #00CFFF;
                color: #1a1a1a;
                border: none;
                border-radius: 8px;
                padding: 15px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #66D9FF;
            }
            QPushButton:pressed {
                background-color: #0099CC;
            }
        """)
        
        self.setup_ui()
        self.center_window()
    
    def setup_ui(self):
        """Setup simple, clean UI"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        
        # Main card
        card = QFrame()
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(25)
        
        # Title
        title = QLabel("🔐 CRYPTEX")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: #00CFFF; margin-bottom: 20px;")
        card_layout.addWidget(title)
        
        # Subtitle
        if pin_exists():
            subtitle_text = "Enter your PIN to unlock"
        else:
            subtitle_text = "Create a secure PIN (4-6 digits)"
        
        subtitle = QLabel(subtitle_text)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("font-size: 16px; color: #cccccc; margin-bottom: 20px;")
        card_layout.addWidget(subtitle)
        
        # PIN input
        self.pin_input = QLineEdit()
        self.pin_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pin_input.setPlaceholderText("Enter PIN...")
        self.pin_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pin_input.setMaxLength(6)
        self.pin_input.returnPressed.connect(self.handle_pin)
        card_layout.addWidget(self.pin_input)
        
        # Button
        if pin_exists():
            button_text = "🔓 Unlock Vault"
        else:
            button_text = "🔐 Create PIN"
        
        self.submit_btn = QPushButton(button_text)
        self.submit_btn.clicked.connect(self.handle_pin)
        card_layout.addWidget(self.submit_btn)
        
        # Security info
        info = QLabel("🛡️ Your data is encrypted with military-grade security")
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info.setStyleSheet("font-size: 12px; color: #888888; margin-top: 20px;")
        card_layout.addWidget(info)
        
        main_layout.addWidget(card)
        self.setLayout(main_layout)
        
        # Focus PIN input
        self.pin_input.setFocus()
    
    def center_window(self):
        """Center window on screen"""
        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )
    
    def handle_pin(self):
        """Handle PIN creation or login"""
        pin = self.pin_input.text().strip()
        
        if not pin:
            self.show_error("Please enter a PIN")
            return
        
        if not pin.isdigit():
            self.show_error("PIN must contain only numbers")
            return
        
        try:
            if pin_exists():
                # Login
                if check_pin(pin):
                    self.login_success(pin)
                else:
                    self.show_error("Incorrect PIN")
            else:
                # Create PIN
                if len(pin) < 4:
                    self.show_error("PIN must be at least 4 digits")
                    return
                if len(pin) > 6:
                    self.show_error("PIN must be at most 6 digits")
                    return
                
                set_pin(pin)
                self.login_success(pin)
        except Exception as e:
            self.show_error(f"Error: {str(e)}")
    
    def login_success(self, pin):
        """Handle successful login"""
        try:
            from gui.dashboard import Dashboard
            self.dashboard = Dashboard(pin)
            self.dashboard.show()
            self.close()
        except Exception as e:
            self.show_error(f"Failed to open dashboard: {str(e)}")
    
    def show_error(self, message):
        """Show error message"""
        self.pin_input.setStyleSheet("""
            QLineEdit {
                background-color: #333333;
                border: 2px solid #ff4444;
                border-radius: 8px;
                padding: 15px;
                font-size: 18px;
                color: white;
            }
        """)
        self.pin_input.setPlaceholderText(message)
        self.pin_input.clear()
        
        # Reset style after 3 seconds
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(3000, self.reset_input_style)
    
    def reset_input_style(self):
        """Reset input style to normal"""
        self.pin_input.setStyleSheet("""
            QLineEdit {
                background-color: #333333;
                border: 2px solid #00CFFF;
                border-radius: 8px;
                padding: 15px;
                font-size: 18px;
                color: white;
            }
            QLineEdit:focus {
                border-color: #66D9FF;
            }
        """)
        self.pin_input.setPlaceholderText("Enter PIN...")
    
    def keyPressEvent(self, event):
        """Handle key press events"""
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        super().keyPressEvent(event)
    
    def closeEvent(self, event):
        """Handle close event"""
        QApplication.quit()
        event.accept()