"""
Modern, clean login window for Cryptex
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QFrame, QApplication,
                            QComboBox, QSpacerItem, QSizePolicy)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPixmap, QPainter, QColor
import os
from core.auth import check_pin, set_pin, pin_exists
from assets.themes import THEMES, generate_qss
from gui.animations import animator
from core.settings import settings

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("LoginWindow")
        self.setWindowTitle("Cryptex - Secure Vault")
        self.setFixedSize(500, 700)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        
        # Load theme
        current_theme = settings.get("theme", "cyber_blue")
        self.apply_theme(current_theme)
        
        self.setup_ui()
        self.center_window()
        
        # Animate window appearance
        animator.fade_in(self, 400)
    
    def apply_theme(self, theme_name):
        """Apply the selected theme"""
        self.setStyleSheet(generate_qss(theme_name))
        settings.set("theme", theme_name)
    
    def setup_ui(self):
        """Setup the beautiful login interface"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(0)
        
        # Close button
        close_layout = QHBoxLayout()
        close_layout.addStretch()
        
        close_btn = QPushButton("✕")
        close_btn.setObjectName("SecondaryButton")
        close_btn.setFixedSize(40, 40)
        close_btn.clicked.connect(self.close)
        close_layout.addWidget(close_btn)
        
        main_layout.addLayout(close_layout)
        main_layout.addSpacing(20)
        
        # Main card
        card = QFrame()
        card.setObjectName("MainCard")
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(30)
        card_layout.setContentsMargins(40, 40, 40, 40)
        
        # Title
        title = QLabel("🔐 CRYPTEX")
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(title)
        
        # Subtitle
        if pin_exists():
            subtitle_text = "Enter your PIN to unlock your secure vault"
        else:
            subtitle_text = "Create a secure PIN to protect your vault"
        
        subtitle = QLabel(subtitle_text)
        subtitle.setObjectName("Subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setWordWrap(True)
        card_layout.addWidget(subtitle)
        
        # PIN input
        self.pin_input = QLineEdit()
        self.pin_input.setObjectName("PinInput")
        self.pin_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pin_input.setPlaceholderText("Enter PIN...")
        self.pin_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pin_input.setMaxLength(6)
        self.pin_input.returnPressed.connect(self.handle_pin)
        self.pin_input.textChanged.connect(self.on_pin_changed)
        card_layout.addWidget(self.pin_input)
        
        # Button
        if pin_exists():
            button_text = "🔓 Unlock Vault"
        else:
            button_text = "🔐 Create PIN"
        
        self.submit_btn = QPushButton(button_text)
        self.submit_btn.setObjectName("PrimaryButton")
        self.submit_btn.clicked.connect(self.handle_pin)
        self.submit_btn.setEnabled(False)
        card_layout.addWidget(self.submit_btn)
        
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
        
        card_layout.addLayout(theme_layout)
        
        # Security info
        info = QLabel("🛡️ Military-grade encryption • 🔒 Offline storage • 🚫 No data collection")
        info.setObjectName("InfoLabel")
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info.setWordWrap(True)
        card_layout.addWidget(info)
        
        main_layout.addWidget(card)
        main_layout.addStretch()
        
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
    
    def on_pin_changed(self):
        """Handle PIN input changes"""
        pin = self.pin_input.text().strip()
        
        # Only allow digits
        if pin and not pin.isdigit():
            # Remove non-digit characters
            clean_pin = ''.join(c for c in pin if c.isdigit())
            self.pin_input.setText(clean_pin)
            return
        
        # Enable button if PIN has minimum length
        min_length = 4 if not pin_exists() else 1
        self.submit_btn.setEnabled(len(pin) >= min_length)
        
        # Visual feedback for PIN length
        if not pin_exists() and len(pin) > 0:
            if len(pin) < 4:
                self.pin_input.setObjectName("ErrorInput")
            else:
                self.pin_input.setObjectName("PinInput")
            self.pin_input.setStyleSheet(self.styleSheet())
    
    def on_theme_changed(self):
        """Handle theme change"""
        theme_key = self.theme_combo.currentData()
        if theme_key:
            self.apply_theme(theme_key)
            animator.pulse_widget(self.theme_combo)
    
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
            # Success animation
            animator.pulse_widget(self.submit_btn)
            
            # Small delay for animation
            QTimer.singleShot(200, lambda: self.open_dashboard(pin))
        except Exception as e:
            self.show_error(f"Failed to open dashboard: {str(e)}")
    
    def open_dashboard(self, pin):
        """Open the dashboard"""
        try:
            from gui.dashboard import Dashboard
            self.dashboard = Dashboard(pin)
            self.dashboard.show()
            
            # Fade out login window
            fade_animation = animator.fade_out(self, 300)
            fade_animation.finished.connect(self.close)
        except Exception as e:
            self.show_error(f"Failed to open dashboard: {str(e)}")
    
    def show_error(self, message):
        """Show error message with animation"""
        # Change input style to error
        self.pin_input.setObjectName("ErrorInput")
        self.pin_input.setStyleSheet(self.styleSheet())
        self.pin_input.setPlaceholderText(message)
        self.pin_input.clear()
        
        # Shake animation
        animator.shake_widget(self.pin_input)
        
        # Reset style after 3 seconds
        QTimer.singleShot(3000, self.reset_input_style)
    
    def reset_input_style(self):
        """Reset input style to normal"""
        self.pin_input.setObjectName("PinInput")
        self.pin_input.setStyleSheet(self.styleSheet())
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