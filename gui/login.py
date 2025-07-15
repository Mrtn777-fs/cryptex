"""
Modern, clean login window for Cryptex
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QFrame, QApplication,
                            QComboBox, QMessageBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
import os
from core.auth import check_pin, set_pin, pin_exists
from assets.themes import THEMES, generate_qss
from core.settings import settings

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cryptex - Secure Vault")
        self.setFixedSize(500, 600)
        
        # Load theme
        current_theme = settings.get("theme", "cyber_blue")
        self.apply_theme(current_theme)
        
        self.setup_ui()
        self.center_window()
    
    def apply_theme(self, theme_name):
        """Apply the selected theme"""
        try:
            self.setStyleSheet(generate_qss(theme_name))
            settings.set("theme", theme_name)
        except Exception as e:
            print(f"Theme error: {e}")
            # Fallback theme
            self.setStyleSheet("""
                QWidget {
                    background-color: #1a1a1a;
                    color: white;
                    font-family: 'Segoe UI';
                }
                QPushButton {
                    background-color: #00CFFF;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 12px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #0099CC;
                }
                QLineEdit {
                    background-color: #2a2a2a;
                    border: 2px solid #00CFFF;
                    border-radius: 8px;
                    padding: 15px;
                    font-size: 24px;
                    color: white;
                }
            """)
    
    def setup_ui(self):
        """Setup the login interface"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)
        
        # Title
        title = QLabel("🔐 CRYPTEX")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 36px; font-weight: bold; color: #00CFFF; margin-bottom: 20px;")
        main_layout.addWidget(title)
        
        # Subtitle
        if pin_exists():
            subtitle_text = "Enter your PIN to unlock your secure vault"
        else:
            subtitle_text = "Create a secure PIN to protect your vault"
        
        subtitle = QLabel(subtitle_text)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet("font-size: 16px; color: #cccccc; margin-bottom: 30px;")
        main_layout.addWidget(subtitle)
        
        # PIN input
        self.pin_input = QLineEdit()
        self.pin_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pin_input.setPlaceholderText("Enter PIN...")
        self.pin_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pin_input.setMaxLength(6)
        self.pin_input.returnPressed.connect(self.handle_pin)
        self.pin_input.textChanged.connect(self.on_pin_changed)
        main_layout.addWidget(self.pin_input)
        
        # Button
        if pin_exists():
            button_text = "🔓 Unlock Vault"
        else:
            button_text = "🔐 Create PIN"
        
        self.submit_btn = QPushButton(button_text)
        self.submit_btn.clicked.connect(self.handle_pin)
        self.submit_btn.setEnabled(False)
        main_layout.addWidget(self.submit_btn)
        
        # Theme selector
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel("Theme:"))
        
        self.theme_combo = QComboBox()
        for theme_key, theme_data in THEMES.items():
            self.theme_combo.addItem(theme_data["name"], theme_key)
        
        # Set current theme
        current_theme = settings.get("theme", "cyber_blue")
        for i in range(self.theme_combo.count()):
            if self.theme_combo.itemData(i) == current_theme:
                self.theme_combo.setCurrentIndex(i)
                break
        
        self.theme_combo.currentTextChanged.connect(self.on_theme_changed)
        theme_layout.addWidget(self.theme_combo)
        theme_layout.addStretch()
        
        main_layout.addLayout(theme_layout)
        
        # Security info
        info = QLabel("🛡️ Military-grade encryption • 🔒 Offline storage • 🚫 No data collection")
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info.setWordWrap(True)
        info.setStyleSheet("font-size: 12px; color: #888888;")
        main_layout.addWidget(info)
        
        self.setLayout(main_layout)
        
        # Focus PIN input
        self.pin_input.setFocus()
    
    def center_window(self):
        """Center window on screen"""
        try:
            screen = QApplication.primaryScreen().geometry()
            size = self.geometry()
            self.move(
                (screen.width() - size.width()) // 2,
                (screen.height() - size.height()) // 2
            )
        except Exception as e:
            print(f"Window centering error: {e}")
    
    def on_pin_changed(self):
        """Handle PIN input changes"""
        try:
            pin = self.pin_input.text().strip()
            
            # Only allow digits
            if pin and not pin.isdigit():
                clean_pin = ''.join(c for c in pin if c.isdigit())
                self.pin_input.setText(clean_pin)
                return
            
            # Enable button if PIN has minimum length
            min_length = 4 if not pin_exists() else 1
            self.submit_btn.setEnabled(len(pin) >= min_length)
        except Exception as e:
            print(f"PIN change error: {e}")
    
    def on_theme_changed(self):
        """Handle theme change"""
        try:
            theme_key = self.theme_combo.currentData()
            if theme_key:
                self.apply_theme(theme_key)
        except Exception as e:
            print(f"Theme change error: {e}")
    
    def handle_pin(self):
        """Handle PIN creation or login"""
        try:
            pin = self.pin_input.text().strip()
            
            if not pin:
                self.show_error("Please enter a PIN")
                return
            
            if not pin.isdigit():
                self.show_error("PIN must contain only numbers")
                return
            
            if pin_exists():
                # Login
                if check_pin(pin):
                    self.submit_btn.setText("✅ Success!")
                    QTimer.singleShot(500, lambda: self.open_dashboard(pin))
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
                
                if set_pin(pin):
                    self.submit_btn.setText("✅ PIN Created!")
                    QTimer.singleShot(500, lambda: self.open_dashboard(pin))
                else:
                    self.show_error("Failed to create PIN")
        except Exception as e:
            print(f"PIN handling error: {e}")
            self.show_error("An error occurred. Please try again.")
    
    def open_dashboard(self, pin):
        """Open the dashboard"""
        try:
            from gui.dashboard import Dashboard
            self.dashboard = Dashboard(pin)
            self.dashboard.show()
            self.close()
        except Exception as e:
            print(f"Dashboard creation error: {e}")
            self.show_error("Failed to open dashboard. Please restart the app.")
    
    def show_error(self, message):
        """Show error message"""
        try:
            self.pin_input.setStyleSheet("""
                QLineEdit {
                    background-color: #2a2a2a;
                    border: 2px solid #ff4444;
                    border-radius: 8px;
                    padding: 15px;
                    font-size: 24px;
                    color: white;
                }
            """)
            self.pin_input.setPlaceholderText(message)
            self.pin_input.clear()
            
            # Reset style after 3 seconds
            QTimer.singleShot(3000, self.reset_input_style)
        except Exception as e:
            print(f"Error display error: {e}")
    
    def reset_input_style(self):
        """Reset input style to normal"""
        try:
            self.pin_input.setStyleSheet("""
                QLineEdit {
                    background-color: #2a2a2a;
                    border: 2px solid #00CFFF;
                    border-radius: 8px;
                    padding: 15px;
                    font-size: 24px;
                    color: white;
                }
            """)
            self.pin_input.setPlaceholderText("Enter PIN...")
        except Exception as e:
            print(f"Style reset error: {e}")
    
    def keyPressEvent(self, event):
        """Handle key press events"""
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        super().keyPressEvent(event)
    
    def closeEvent(self, event):
        """Handle close event"""
        QApplication.quit()
        event.accept()