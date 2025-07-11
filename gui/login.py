from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QFrame, QCheckBox, QApplication)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QKeySequence, QShortcut
import os
from core.auth import check_pin, set_pin, pin_exists
from gui.dashboard import Dashboard

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.pin = None
        self.failed_attempts = 0
        self.max_attempts = 5
        
        self.setWindowTitle("Cryptex - Secure Login")
        self.setFixedSize(450, 600)
        
        # Simple, clean styling that actually works
        self.setStyleSheet("""
            QWidget {
                background-color: #1a1a1a;
                color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
            
            QFrame#main-card {
                background-color: #2d2d2d;
                border: 1px solid #4a4a4a;
                border-radius: 10px;
                padding: 30px;
                margin: 20px;
            }
            
            QLabel#title {
                font-size: 32px;
                font-weight: bold;
                color: #6366f1;
                margin: 10px 0;
            }
            
            QLabel#subtitle {
                font-size: 16px;
                color: #a0a0a0;
                margin-bottom: 20px;
            }
            
            QLineEdit {
                background-color: #3a3a3a;
                border: 2px solid #555555;
                border-radius: 8px;
                padding: 15px;
                font-size: 18px;
                color: #ffffff;
                min-height: 20px;
            }
            
            QLineEdit:focus {
                border: 2px solid #6366f1;
                background-color: #404040;
            }
            
            QPushButton {
                background-color: #6366f1;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 15px;
                font-size: 16px;
                font-weight: bold;
                min-height: 20px;
            }
            
            QPushButton:hover {
                background-color: #7c3aed;
            }
            
            QPushButton:pressed {
                background-color: #4f46e5;
            }
            
            QPushButton#close-btn {
                background-color: #dc2626;
                border-radius: 15px;
                padding: 8px;
                font-size: 16px;
                font-weight: bold;
                max-width: 30px;
                max-height: 30px;
            }
            
            QPushButton#close-btn:hover {
                background-color: #ef4444;
            }
            
            QCheckBox {
                color: #a0a0a0;
                font-size: 14px;
                spacing: 10px;
            }
            
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #6366f1;
                border-radius: 3px;
                background-color: #3a3a3a;
            }
            
            QCheckBox::indicator:checked {
                background-color: #6366f1;
            }
            
            QLabel#error {
                color: #ef4444;
                background-color: #2d1b1b;
                border: 1px solid #ef4444;
                border-radius: 6px;
                padding: 10px;
                font-weight: bold;
                margin: 10px 0;
            }
            
            QLabel#success {
                color: #10b981;
                background-color: #1b2d1b;
                border: 1px solid #10b981;
                border-radius: 6px;
                padding: 10px;
                font-weight: bold;
                margin: 10px 0;
            }
            
            QLabel#info {
                color: #a0a0a0;
                font-size: 12px;
                margin: 5px 0;
            }
        """)
        
        self.setup_ui()
        self.center_window()
        
        # Add keyboard shortcuts
        self.setup_shortcuts()
    
    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Main card
        card = QFrame()
        card.setObjectName("main-card")
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(20)
        
        # Header with close button
        header_layout = QHBoxLayout()
        header_layout.addStretch()
        
        close_btn = QPushButton("×")
        close_btn.setObjectName("close-btn")
        close_btn.setFixedSize(30, 30)
        close_btn.clicked.connect(self.close)
        close_btn.setToolTip("Close Application")
        header_layout.addWidget(close_btn)
        
        card_layout.addLayout(header_layout)
        
        # Logo and title section
        logo_layout = QVBoxLayout()
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.setSpacing(15)
        
        # Logo
        logo = QLabel("🔐")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setStyleSheet("font-size: 80px; margin: 20px 0;")
        logo_layout.addWidget(logo)
        
        # Title
        title = QLabel("CRYPTEX")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Secure Note Manager")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(subtitle)
        
        card_layout.addLayout(logo_layout)
        
        # Status message area
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.hide()
        card_layout.addWidget(self.status_label)
        
        # PIN input section
        pin_section = QVBoxLayout()
        pin_section.setSpacing(15)
        
        # PIN instruction
        self.pin_instruction = QLabel()
        self.update_pin_instruction()
        self.pin_instruction.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pin_instruction.setStyleSheet("font-size: 18px; font-weight: bold; color: #ffffff; margin: 15px 0;")
        pin_section.addWidget(self.pin_instruction)
        
        # PIN input field
        self.pin_input = QLineEdit()
        self.pin_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pin_input.setPlaceholderText("Enter your PIN here...")
        self.pin_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pin_input.returnPressed.connect(self.handle_login)
        self.pin_input.textChanged.connect(self.on_pin_changed)
        pin_section.addWidget(self.pin_input)
        
        # Show PIN checkbox (only for setup)
        if not pin_exists():
            self.show_pin_cb = QCheckBox("Show PIN while typing")
            self.show_pin_cb.toggled.connect(self.toggle_pin_visibility)
            pin_section.addWidget(self.show_pin_cb)
        
        card_layout.addLayout(pin_section)
        
        # Action button
        self.action_button = QPushButton()
        self.update_action_button()
        self.action_button.clicked.connect(self.handle_login)
        card_layout.addWidget(self.action_button)
        
        # Security features info
        info_section = QVBoxLayout()
        info_section.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_section.setSpacing(8)
        
        info_title = QLabel("Security Features:")
        info_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_title.setStyleSheet("font-size: 14px; font-weight: bold; color: #ffffff; margin: 20px 0 10px 0;")
        info_section.addWidget(info_title)
        
        features = [
            "🔒 AES-256 Encryption",
            "💾 Local Storage Only", 
            "🛡️ Zero Data Collection",
            "🔐 PIN-Based Security"
        ]
        
        for feature in features:
            label = QLabel(feature)
            label.setObjectName("info")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            info_section.addWidget(label)
        
        card_layout.addLayout(info_section)
        
        # Instructions
        instructions = QLabel("Press Enter to continue or Escape to exit")
        instructions.setObjectName("info")
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instructions.setStyleSheet("margin-top: 20px;")
        card_layout.addWidget(instructions)
        
        main_layout.addWidget(card)
        self.setLayout(main_layout)
        
        # Focus PIN input
        self.pin_input.setFocus()
    
    def setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        # Escape to close
        escape_shortcut = QShortcut(QKeySequence("Escape"), self)
        escape_shortcut.activated.connect(self.close)
        
        # Ctrl+Q to quit
        quit_shortcut = QShortcut(QKeySequence("Ctrl+Q"), self)
        quit_shortcut.activated.connect(self.close)
    
    def update_pin_instruction(self):
        """Update PIN instruction based on current state"""
        if pin_exists():
            self.pin_instruction.setText("Enter your PIN to unlock")
        else:
            self.pin_instruction.setText("Create a secure PIN (minimum 4 characters)")
    
    def update_action_button(self):
        """Update action button text based on current state"""
        if pin_exists():
            self.action_button.setText("🔓 Unlock Vault")
        else:
            self.action_button.setText("🔐 Create PIN & Setup Vault")
    
    def center_window(self):
        """Center window on screen"""
        screen = self.screen().availableGeometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )
    
    def toggle_pin_visibility(self, checked):
        """Toggle PIN visibility"""
        if checked:
            self.pin_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.pin_input.setEchoMode(QLineEdit.EchoMode.Password)
    
    def on_pin_changed(self):
        """Handle PIN input changes"""
        pin = self.pin_input.text()
        if not pin_exists() and len(pin) >= 4:
            self.action_button.setEnabled(True)
        elif pin_exists() and len(pin) > 0:
            self.action_button.setEnabled(True)
        else:
            self.action_button.setEnabled(len(pin) > 0)
    
    def handle_login(self):
        """Handle login/setup process"""
        pin = self.pin_input.text().strip()
        
        if not pin:
            self.show_error("Please enter a PIN")
            return
        
        if pin_exists():
            # Login mode
            if check_pin(pin):
                self.login_success(pin)
            else:
                self.login_failed()
        else:
            # Setup mode
            if len(pin) < 4:
                self.show_error("PIN must be at least 4 characters long")
                return
            
            try:
                set_pin(pin)
                self.show_success("PIN created successfully! Opening your vault...")
                QTimer.singleShot(1500, lambda: self.login_success(pin))
            except Exception as e:
                self.show_error(f"Failed to create PIN: {str(e)}")
    
    def login_success(self, pin):
        """Handle successful login"""
        self.pin = pin
        self.show_success("Access granted! Loading your secure vault...")
        
        def open_dashboard():
            try:
                self.dashboard = Dashboard(pin)
                self.dashboard.show()
                self.close()
            except Exception as e:
                self.show_error(f"Failed to open vault: {str(e)}")
        
        QTimer.singleShot(1000, open_dashboard)
    
    def login_failed(self):
        """Handle failed login attempt"""
        self.failed_attempts += 1
        remaining = self.max_attempts - self.failed_attempts
        
        if remaining > 0:
            self.show_error(f"❌ Incorrect PIN! {remaining} attempts remaining")
            self.pin_input.clear()
            self.pin_input.setFocus()
        else:
            self.show_error("🚫 Too many failed attempts! Please restart the application")
            self.action_button.setEnabled(False)
            self.pin_input.setEnabled(False)
    
    def show_error(self, message):
        """Show error message"""
        self.status_label.setText(message)
        self.status_label.setObjectName("error")
        self.status_label.setStyleSheet(self.status_label.styleSheet())
        self.status_label.show()
        
        # Clear after 4 seconds
        QTimer.singleShot(4000, lambda: self.status_label.hide())
    
    def show_success(self, message):
        """Show success message"""
        self.status_label.setText(message)
        self.status_label.setObjectName("success")
        self.status_label.setStyleSheet(self.status_label.styleSheet())
        self.status_label.show()
    
    def keyPressEvent(self, event):
        """Handle key press events"""
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        elif event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            if self.action_button.isEnabled():
                self.handle_login()
        super().keyPressEvent(event)
    
    def closeEvent(self, event):
        """Handle close event"""
        QApplication.quit()
        event.accept()