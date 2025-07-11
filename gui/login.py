from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QFrame, QProgressBar, 
                            QCheckBox, QGraphicsOpacityEffect, QSpacerItem, QSizePolicy)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPropertyAnimation, QEasingCurve, QRect
from PyQt6.QtGui import QFont, QPalette
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
        self.animation = None
        
        self.setWindowTitle("Cryptex - Secure Login")
        self.setFixedSize(500, 700)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        
        # Apply theme
        current_theme = settings.get("theme", "dark_modern")
        self.setStyleSheet(generate_qss(current_theme))
        
        self.setup_ui()
        self.center_window()
        self.setup_animations()
    
    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Main container with gradient background
        container = QFrame()
        container.setObjectName("login-card")
        container.setStyleSheet(f"""
            QFrame#login-card {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1a1a2e, stop:1 #0f0f23);
                border-radius: 24px;
                border: 2px solid #6366f1;
            }}
        """)
        
        layout = QVBoxLayout(container)
        layout.setSpacing(30)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Header section
        self.setup_header(layout)
        
        # Login form section
        self.setup_login_form(layout)
        
        # Footer section
        self.setup_footer(layout)
        
        main_layout.addWidget(container)
        self.setLayout(main_layout)
    
    def setup_header(self, layout):
        """Setup modern header with logo and title"""
        header_layout = QVBoxLayout()
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.setSpacing(20)
        
        # Logo container
        logo_container = QFrame()
        logo_container.setFixedSize(120, 120)
        logo_container.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #6366f1, stop:1 #8b5cf6);
                border-radius: 60px;
                border: 3px solid #a855f7;
            }
        """)
        
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        
        # Logo icon
        logo = QLabel("🔐")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setStyleSheet("font-size: 48px; background: transparent; border: none;")
        logo_layout.addWidget(logo)
        
        # Center the logo container
        logo_center_layout = QHBoxLayout()
        logo_center_layout.addStretch()
        logo_center_layout.addWidget(logo_container)
        logo_center_layout.addStretch()
        header_layout.addLayout(logo_center_layout)
        
        # Title
        title = QLabel("CRYPTEX")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 42px; 
            font-weight: 800; 
            color: #6366f1;
            letter-spacing: 3px;
            margin: 10px 0;
        """)
        header_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Secure Note Manager")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("""
            font-size: 18px; 
            color: #a1a1aa;
            font-weight: 500;
            margin-bottom: 10px;
        """)
        header_layout.addWidget(subtitle)
        
        # Version badge
        version_badge = QLabel("v2.0 Enhanced")
        version_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version_badge.setStyleSheet("""
            background-color: #6366f1;
            color: white;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            margin: 10px 0;
        """)
        version_badge.setFixedWidth(120)
        
        version_center_layout = QHBoxLayout()
        version_center_layout.addStretch()
        version_center_layout.addWidget(version_badge)
        version_center_layout.addStretch()
        header_layout.addLayout(version_center_layout)
        
        layout.addLayout(header_layout)
    
    def setup_login_form(self, layout):
        """Setup modern login form"""
        form_layout = QVBoxLayout()
        form_layout.setSpacing(25)
        
        # Status label
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
            color: #ef4444; 
            font-weight: 600; 
            font-size: 14px;
            min-height: 25px;
            padding: 8px;
            border-radius: 8px;
        """)
        form_layout.addWidget(self.status_label)
        
        # PIN input section
        pin_section = QVBoxLayout()
        pin_section.setSpacing(15)
        
        # PIN label
        self.pin_label = QLabel("Enter your PIN" if pin_exists() else "Create a secure PIN")
        self.pin_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pin_label.setStyleSheet("""
            font-size: 18px; 
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 5px;
        """)
        pin_section.addWidget(self.pin_label)
        
        # PIN description
        pin_desc = QLabel("Minimum 4 characters" if not pin_exists() else "Enter your secure PIN to continue")
        pin_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pin_desc.setStyleSheet("""
            font-size: 14px;
            color: #a1a1aa;
            margin-bottom: 10px;
        """)
        pin_section.addWidget(pin_desc)

        # PIN input
        self.pin_input = QLineEdit()
        self.pin_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pin_input.setPlaceholderText("Enter PIN...")
        self.pin_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pin_input.setStyleSheet("""
            QLineEdit {
                font-size: 24px; 
                padding: 20px; 
                font-weight: 600; 
                letter-spacing: 8px;
                text-align: center;
                background-color: #1a1a2e;
                border: 3px solid #374151;
                border-radius: 16px;
                color: #ffffff;
            }
            QLineEdit:focus {
                border: 3px solid #6366f1;
                background-color: #16213e;
            }
            QLineEdit:hover {
                border: 3px solid #7c3aed;
            }
        """)
        self.pin_input.returnPressed.connect(self.handle_login)
        pin_section.addWidget(self.pin_input)
        
        form_layout.addLayout(pin_section)
        
        # Show PIN checkbox (for setup only)
        if not pin_exists():
            checkbox_layout = QHBoxLayout()
            checkbox_layout.addStretch()
            
            self.show_pin_cb = QCheckBox("Show PIN")
            self.show_pin_cb.setStyleSheet("""
                QCheckBox {
                    font-size: 14px; 
                    color: #a1a1aa;
                    font-weight: 500;
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                    border: 2px solid #6366f1;
                    border-radius: 4px;
                    background-color: #1a1a2e;
                }
                QCheckBox::indicator:checked {
                    background-color: #6366f1;
                }
            """)
            self.show_pin_cb.toggled.connect(self.toggle_pin_visibility)
            checkbox_layout.addWidget(self.show_pin_cb)
            checkbox_layout.addStretch()
            form_layout.addLayout(checkbox_layout)
        
        # Login button
        self.login_button = QPushButton("🔓 Login" if pin_exists() else "🔐 Create PIN")
        self.login_button.setStyleSheet("""
            QPushButton {
                font-size: 18px; 
                padding: 18px 32px; 
                font-weight: 700;
                border-radius: 16px;
                min-height: 25px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6366f1, stop:1 #8b5cf6);
                color: white;
                border: none;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #7c3aed, stop:1 #a855f7);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4f46e5, stop:1 #7c2d12);
            }
            QPushButton:disabled {
                background-color: #374151;
                color: #6b7280;
            }
        """)
        self.login_button.clicked.connect(self.handle_login)
        form_layout.addWidget(self.login_button)
        
        # Progress bar (hidden initially)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 8px;
                background-color: #1a1a2e;
                height: 8px;
                text-align: center;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6366f1, stop:1 #8b5cf6);
                border-radius: 8px;
            }
        """)
        form_layout.addWidget(self.progress_bar)
        
        layout.addLayout(form_layout)
    
    def setup_footer(self, layout):
        """Setup modern footer"""
        footer_layout = QVBoxLayout()
        footer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_layout.setSpacing(15)
        
        # Security features
        features_layout = QVBoxLayout()
        features_layout.setSpacing(8)
        
        features = [
            "🔒 Military-grade AES encryption",
            "🛡️ Zero-knowledge architecture", 
            "💾 Local storage only",
            "🔐 PIN-based authentication"
        ]
        
        for feature in features:
            feature_label = QLabel(feature)
            feature_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            feature_label.setStyleSheet("""
                color: #a1a1aa; 
                font-size: 12px; 
                font-weight: 500;
                margin: 2px 0;
            """)
            features_layout.addWidget(feature_label)
        
        layout.addLayout(features_layout)
        
        # Close button
        close_layout = QHBoxLayout()
        close_layout.addStretch()
        
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(40, 40)
        close_btn.setStyleSheet("""
            QPushButton {
                border-radius: 20px;
                font-size: 16px;
                font-weight: bold;
                background-color: #374151;
                color: #a1a1aa;
                border: none;
            }
            QPushButton:hover {
                background-color: #ef4444;
                color: white;
            }
        """)
        close_btn.clicked.connect(self.close)
        close_layout.addWidget(close_btn)
        
        layout.addLayout(close_layout)
    
    def setup_animations(self):
        """Setup smooth animations"""
        # Fade in animation
        self.opacity_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity_effect)
        
        self.fade_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_animation.setDuration(800)
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.fade_animation.start()
    
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
            self.shake_animation()
            return
        
        # Set loading state
        self.set_loading(True)
        
        # Process login with a small delay for smooth UX
        QTimer.singleShot(500, lambda: self.process_login(pin))
    
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
                    self.shake_animation()
                    return
                
                # Create new PIN
                set_pin(pin)
                self.show_success("PIN created successfully!")
                QTimer.singleShot(1200, lambda: self.login_success(pin))
        except Exception as e:
            self.set_loading(False)
            self.show_error(f"Error: {str(e)}")
            self.shake_animation()
    
    def login_success(self, pin):
        """Handle successful login"""
        self.pin = pin
        self.set_loading(False)
        self.show_success("Access granted! Opening vault...")
        
        # Fade out and open dashboard
        def open_dashboard():
            try:
                self.dashboard = Dashboard(pin)
                self.dashboard.show()
                self.close()
            except Exception as e:
                self.show_error(f"Failed to open dashboard: {str(e)}")
                self.set_loading(False)
        
        QTimer.singleShot(800, open_dashboard)
    
    def login_failed(self):
        """Handle failed login"""
        self.failed_attempts += 1
        self.set_loading(False)
        
        remaining = self.max_attempts - self.failed_attempts
        
        if remaining > 0:
            self.show_error(f"❌ Incorrect PIN. {remaining} attempts remaining.")
            self.shake_animation()
            self.pin_input.clear()
            self.pin_input.setFocus()
        else:
            self.lock_interface()
    
    def lock_interface(self):
        """Lock interface after too many failed attempts"""
        self.is_locked = True
        self.pin_input.setEnabled(False)
        self.login_button.setEnabled(False)
        self.show_error("🚫 Too many failed attempts. Locked for 5 minutes.")
        
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
        """Set loading state with smooth transitions"""
        self.pin_input.setEnabled(not loading)
        self.login_button.setEnabled(not loading)
        
        if loading:
            self.login_button.setText("🔄 Processing...")
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)  # Indeterminate
        else:
            self.login_button.setText("🔓 Login" if pin_exists() else "🔐 Create PIN")
            self.progress_bar.setVisible(False)
    
    def show_error(self, message):
        """Show error message with styling"""
        self.status_label.setText(message)
        self.status_label.setStyleSheet("""
            color: #ef4444; 
            font-weight: 600; 
            font-size: 14px;
            background-color: rgba(239, 68, 68, 0.1);
            border: 1px solid #ef4444;
            border-radius: 8px;
            padding: 12px;
        """)
    
    def show_success(self, message):
        """Show success message with styling"""
        self.status_label.setText(f"✅ {message}")
        self.status_label.setStyleSheet("""
            color: #10b981; 
            font-weight: 600; 
            font-size: 14px;
            background-color: rgba(16, 185, 129, 0.1);
            border: 1px solid #10b981;
            border-radius: 8px;
            padding: 12px;
        """)
    
    def shake_animation(self):
        """Smooth shake animation for errors"""
        if self.animation:
            self.animation.stop()
        
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(500)
        self.animation.setLoopCount(3)
        
        start_geometry = self.geometry()
        
        self.animation.setKeyValueAt(0, start_geometry)
        self.animation.setKeyValueAt(0.25, QRect(start_geometry.x() - 10, start_geometry.y(), start_geometry.width(), start_geometry.height()))
        self.animation.setKeyValueAt(0.75, QRect(start_geometry.x() + 10, start_geometry.y(), start_geometry.width(), start_geometry.height()))
        self.animation.setKeyValueAt(1, start_geometry)
        
        self.animation.start()
    
    def keyPressEvent(self, event):
        """Handle key press events"""
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        super().keyPressEvent(event)