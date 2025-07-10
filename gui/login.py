from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QMessageBox, QFrame,
                            QProgressBar, QCheckBox)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont
import os
from core.auth import check_pin, set_pin, pin_exists
from core.settings import settings
from assets.themes import generate_qss
from gui.dashboard import Dashboard

class LoginWindow(QWidget):
    login_successful = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.pin = None
        self.failed_attempts = 0
        self.max_attempts = 5
        self.is_locked = False
        
        self.setWindowTitle("Cryptex - Login")
        self.setFixedSize(400, 500)
        
        # Apply theme
        current_theme = settings.get("theme", "dark_red")
        self.setStyleSheet(generate_qss(current_theme))
        
        self.setup_ui()
        self.center_window()
    
    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Main container
        container = QFrame()
        container.setObjectName("card")
        layout = QVBoxLayout(container)
        layout.setSpacing(20)
        
        # Header
        self.setup_header(layout)
        
        # Login form
        self.setup_login_form(layout)
        
        # Footer
        self.setup_footer(layout)
        
        main_layout.addWidget(container)
        self.setLayout(main_layout)
    
    def setup_header(self, layout):
        """Setup header with logo and title"""
        header_layout = QVBoxLayout()
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Logo/Icon
        logo = QLabel("🔐")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setStyleSheet("font-size: 48px; margin: 10px;")
        header_layout.addWidget(logo)
        
        # Title
        title = QLabel("CRYPTEX")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Secure Note Manager")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(subtitle)
        
        layout.addLayout(header_layout)
    
    def setup_login_form(self, layout):
        """Setup login form"""
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)
        
        # Status label
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #ff6666; font-weight: bold;")
        form_layout.addWidget(self.status_label)
        
        # PIN input
        self.pin_label = QLabel("Enter PIN" if pin_exists() else "Create a new PIN")
        self.pin_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_layout.addWidget(self.pin_label)

        self.pin_input = QLineEdit()
        self.pin_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pin_input.setPlaceholderText("Enter your PIN...")
        self.pin_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pin_input.setStyleSheet("font-size: 18px; padding: 15px;")
        self.pin_input.returnPressed.connect(self.handle_login)
        form_layout.addWidget(self.pin_input)
        
        # Show PIN checkbox (for setup only)
        if not pin_exists():
            self.show_pin_cb = QCheckBox("Show PIN")
            self.show_pin_cb.toggled.connect(self.toggle_pin_visibility)
            form_layout.addWidget(self.show_pin_cb)
        
        # Login button
        self.login_button = QPushButton("Login" if pin_exists() else "Create PIN")
        self.login_button.setStyleSheet("font-size: 16px; padding: 15px; font-weight: bold;")
        self.login_button.clicked.connect(self.handle_login)
        form_layout.addWidget(self.login_button)
        
        # Progress bar (hidden initially)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("margin: 10px 0;")
        form_layout.addWidget(self.progress_bar)
        
        layout.addLayout(form_layout)
    
    def setup_footer(self, layout):
        """Setup footer"""
        footer_layout = QVBoxLayout()
        footer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Version info
        version_label = QLabel("v2.0 - Enhanced Edition")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version_label.setStyleSheet("color: #888; font-size: 12px; margin-top: 20px;")
        footer_layout.addWidget(version_label)
        
        # Close button
        close_btn = QPushButton("×")
        close_btn.setFixedSize(30, 30)
        close_btn.setStyleSheet("""
            QPushButton {
                border-radius: 15px;
                font-size: 18px;
                font-weight: bold;
                background-color: #666;
            }
            QPushButton:hover {
                background-color: #888;
            }
        """)
        close_btn.clicked.connect(self.close)
        
        close_layout = QHBoxLayout()
        close_layout.addStretch()
        close_layout.addWidget(close_btn)
        footer_layout.addLayout(close_layout)
        
        layout.addLayout(footer_layout)
    
    def center_window(self):
        """Center the window on screen"""
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

    def handle_login(self):
        if self.is_locked:
            return
            
        pin = self.pin_input.text().strip()
        
        if not pin:
            self.show_error("Please enter a PIN")
            return
        
        # Disable input during processing
        self.set_loading(True)
        
        # Process immediately without delay to prevent freezing
        self.process_login(pin)
    
    def process_login(self, pin):
        """Process login"""
        try:
            if pin_exists():
                if check_pin(pin):
                    self.login_success(pin)
                else:
                    self.login_failed()
            else:
                if len(pin) < 4:
                    self.set_loading(False)
                    self.show_error("PIN must be at least 4 characters")
                    return
                
                # Create new PIN
                set_pin(pin)
                self.show_success("PIN created successfully!")
                # Use a short delay before opening dashboard
                QTimer.singleShot(1000, lambda: self.login_success(pin))
        except Exception as e:
            self.set_loading(False)
            self.show_error(f"Error: {str(e)}")
    
    def login_success(self, pin):
        """Handle successful login"""
        self.pin = pin
        self.set_loading(False)
        self.show_success("Login successful!")
        
        # Open dashboard after a short delay
        def open_dashboard():
            try:
                self.dashboard = Dashboard(pin)
                self.dashboard.show()
                self.close()
            except Exception as e:
                self.show_error(f"Failed to open dashboard: {str(e)}")
                self.set_loading(False)
        
        QTimer.singleShot(500, open_dashboard)
    
    def login_failed(self):
        """Handle failed login"""
        self.failed_attempts += 1
        self.set_loading(False)
        
        remaining = self.max_attempts - self.failed_attempts
        
        if remaining > 0:
            self.show_error(f"Incorrect PIN. {remaining} attempts remaining.")
            self.pin_input.clear()
            self.pin_input.setFocus()
        else:
            self.lock_interface()
    
    def lock_interface(self):
        """Lock interface after too many failed attempts"""
        self.is_locked = True
        self.pin_input.setEnabled(False)
        self.login_button.setEnabled(False)
        self.show_error("Too many failed attempts. Interface locked.")
        
        # Auto-unlock after 5 minutes
        QTimer.singleShot(300000, self.unlock_interface)
    
    def unlock_interface(self):
        """Unlock interface"""
        self.is_locked = False
        self.failed_attempts = 0
        self.pin_input.setEnabled(True)
        self.login_button.setEnabled(True)
        self.status_label.clear()
        self.pin_input.setFocus()
    
    def set_loading(self, loading):
        """Set loading state"""
        self.pin_input.setEnabled(not loading)
        self.login_button.setEnabled(not loading)
        
        if loading:
            self.login_button.setText("Processing...")
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)  # Indeterminate
        else:
            self.login_button.setText("Login" if pin_exists() else "Create PIN")
            self.progress_bar.setVisible(False)
    
    def show_error(self, message):
        """Show error message"""
        self.status_label.setText(f"❌ {message}")
        self.status_label.setStyleSheet("color: #ff4444; font-weight: bold;")
    
    def show_success(self, message):
        """Show success message"""
        self.status_label.setText(f"✅ {message}")
        self.status_label.setStyleSheet("color: #44ff44; font-weight: bold;")
    
    def keyPressEvent(self, event):
        """Handle key press events"""
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        super().keyPressEvent(event)