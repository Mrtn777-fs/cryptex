"""Modern glassmorphism login window for Cryptex"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QFrame, QCheckBox, 
                            QApplication, QMessageBox)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QKeySequence, QShortcut
import os
from core.auth import check_pin, set_pin, pin_exists
from gui.dashboard import Dashboard
from assets.themes import get_modern_qss
from gui.animations import ModernAnimator

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.pin = None
        self.failed_attempts = 0
        self.max_attempts = 5
        self.animator = ModernAnimator()
        
        # Setup window
        self.setWindowTitle("Cryptex - Secure Vault")
        self.setFixedSize(500, 700)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Apply modern theme
        self.setStyleSheet(get_modern_qss())
        
        self.setup_ui()
        self.center_window()
        self.setup_shortcuts()
        
        # Animate entrance
        self.animator.fade_in(self, 800)
    
    def setup_ui(self):
        """Setup modern glassmorphism UI"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Main glass panel
        glass_panel = QFrame()
        glass_panel.setStyleSheet("""
            QFrame {
                background: rgba(26, 26, 46, 0.85);
                border: 2px solid rgba(0, 207, 255, 0.3);
                border-radius: 24px;
                padding: 40px;
            }
        """)
        panel_layout = QVBoxLayout(glass_panel)
        panel_layout.setSpacing(30)
        
        # Header with close button
        header_layout = QHBoxLayout()
        header_layout.addStretch()
        
        close_btn = QPushButton("×")
        close_btn.setStyleSheet("""
            QPushButton {
                background: rgba(239, 68, 68, 0.8);
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 18px;
                font-weight: bold;
                min-width: 40px;
                min-height: 40px;
                max-width: 40px;
                max-height: 40px;
            }
            QPushButton:hover {
                background: rgba(239, 68, 68, 1.0);
            }
        """)
        close_btn.clicked.connect(self.close)
        close_btn.setToolTip("Close Application")
        header_layout.addWidget(close_btn)
        
        panel_layout.addLayout(header_layout)
        
        # Logo and branding
        branding_layout = QVBoxLayout()
        branding_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        branding_layout.setSpacing(20)
        
        # Cryptex logo
        logo = QLabel("🔐")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setStyleSheet("""
            font-size: 80px;
            margin: 20px 0;
            color: #00CFFF;
        """)
        branding_layout.addWidget(logo)
        
        # Title
        title = QLabel("CRYPTEX")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 36px;
            font-weight: 700;
            color: #00CFFF;
            margin: 20px 0;
        """)
        branding_layout.addWidget(title)
        
        # Subtitle
        subtitle_text = "Create your PIN" if not pin_exists() else "Enter your PIN"
        subtitle = QLabel(subtitle_text)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("""
            font-size: 18px;
            font-weight: 500;
            color: #A1A1AA;
            margin: 10px 0;
        """)
        branding_layout.addWidget(subtitle)
        
        panel_layout.addLayout(branding_layout)
        
        # PIN input section
        pin_section = QVBoxLayout()
        pin_section.setSpacing(25)
        
        # PIN instruction
        instruction_text = "Set a secure PIN (4-6 digits)" if not pin_exists() else "Enter your PIN to unlock"
        self.pin_instruction = QLabel(instruction_text)
        self.pin_instruction.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pin_instruction.setStyleSheet("""
            font-size: 16px;
            font-weight: 500;
            color: #A1A1AA;
            margin: 10px 0;
        """)
        pin_section.addWidget(self.pin_instruction)
        
        # PIN input field
        self.pin_input = QLineEdit()
        self.pin_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pin_input.setPlaceholderText("••••••")
        self.pin_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pin_input.setMaxLength(6)
        self.pin_input.setStyleSheet("""
            QLineEdit {
                background: rgba(26, 26, 46, 0.6);
                border: 2px solid rgba(0, 207, 255, 0.4);
                border-radius: 16px;
                padding: 20px 24px;
                font-size: 24px;
                font-weight: 600;
                color: white;
                letter-spacing: 8px;
            }
            QLineEdit:focus {
                border: 2px solid #00CFFF;
                background: rgba(26, 26, 46, 0.9);
            }
        """)
        self.pin_input.returnPressed.connect(self.handle_login)
        self.pin_input.textChanged.connect(self.on_pin_changed)
        pin_section.addWidget(self.pin_input)
        
        # Show PIN checkbox (only for setup)
        if not pin_exists():
            checkbox_layout = QHBoxLayout()
            checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            self.show_pin_cb = QCheckBox("Show PIN while typing")
            self.show_pin_cb.setStyleSheet("""
                QCheckBox {
                    color: #A1A1AA;
                    font-size: 14px;
                    font-weight: 500;
                    spacing: 12px;
                }
                QCheckBox::indicator {
                    width: 20px;
                    height: 20px;
                    border: 2px solid rgba(0, 207, 255, 0.5);
                    border-radius: 6px;
                    background: rgba(26, 26, 46, 0.6);
                }
                QCheckBox::indicator:checked {
                    background: #00CFFF;
                    border: 2px solid #00CFFF;
                }
            """)
            self.show_pin_cb.toggled.connect(self.toggle_pin_visibility)
            checkbox_layout.addWidget(self.show_pin_cb)
            pin_section.addLayout(checkbox_layout)
        
        panel_layout.addLayout(pin_section)
        
        # Action button
        button_text = "🔐 Create Secure PIN" if not pin_exists() else "🔓 Unlock Vault"
        self.action_button = QPushButton(button_text)
        self.action_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00CFFF, stop:1 #8B5CF6);
                color: white;
                border: none;
                border-radius: 16px;
                padding: 18px 32px;
                font-size: 16px;
                font-weight: 600;
                min-height: 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(0, 207, 255, 0.9), stop:1 rgba(139, 92, 246, 0.9));
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(0, 207, 255, 0.7), stop:1 rgba(139, 92, 246, 0.7));
            }
            QPushButton:disabled {
                background: rgba(107, 114, 128, 0.5);
                color: rgba(255, 255, 255, 0.5);
            }
        """)
        self.action_button.clicked.connect(self.handle_login)
        self.action_button.setEnabled(False)
        panel_layout.addWidget(self.action_button)
        
        # Security features
        features_layout = QVBoxLayout()
        features_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        features_layout.setSpacing(12)
        
        features_title = QLabel("🛡️ Security Features")
        features_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        features_title.setStyleSheet("""
            font-size: 16px;
            font-weight: 600;
            color: #00CFFF;
            margin: 20px 0 10px 0;
        """)
        features_layout.addWidget(features_title)
        
        features = [
            "🔒 Military-grade AES-256 encryption",
            "💾 100% offline - your data stays local", 
            "🚫 Zero telemetry or data collection",
            "⚡ Instant PIN-based authentication"
        ]
        
        for feature in features:
            label = QLabel(feature)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("""
                font-size: 14px;
                color: #A1A1AA;
                padding: 8px 0;
            """)
            features_layout.addWidget(label)
        
        panel_layout.addLayout(features_layout)
        
        # Footer
        footer = QLabel("Press Enter to continue • Escape to exit")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet("""
            color: #6B7280;
            font-size: 12px;
            font-weight: 400;
            margin-top: 20px;
        """)
        panel_layout.addWidget(footer)
        
        main_layout.addWidget(glass_panel)
        self.setLayout(main_layout)
        
        # Focus PIN input
        self.pin_input.setFocus()
    
    def setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        escape_shortcut = QShortcut(QKeySequence("Escape"), self)
        escape_shortcut.activated.connect(self.close)
        
        quit_shortcut = QShortcut(QKeySequence("Ctrl+Q"), self)
        quit_shortcut.activated.connect(self.close)
    
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
        
        # Only allow digits
        filtered_pin = ''.join(c for c in pin if c.isdigit())
        if filtered_pin != pin:
            self.pin_input.setText(filtered_pin)
            return
        
        # Enable button based on PIN length
        if not pin_exists():
            self.action_button.setEnabled(len(filtered_pin) >= 4)
        else:
            self.action_button.setEnabled(len(filtered_pin) > 0)
    
    def handle_login(self):
        """Handle login/setup process"""
        pin = self.pin_input.text().strip()
        
        if not pin:
            self.show_error("Please enter a PIN")
            return
        
        if not pin.isdigit():
            self.show_error("PIN must contain only digits")
            return
        
        try:
            if pin_exists():
                # Login mode
                if check_pin(pin):
                    self.login_success(pin)
                else:
                    self.login_failed()
            else:
                # Setup mode
                if len(pin) < 4:
                    self.show_error("PIN must be at least 4 digits long")
                    return
                
                if len(pin) > 6:
                    self.show_error("PIN must be at most 6 digits long")
                    return
                
                set_pin(pin)
                self.show_success("PIN created successfully!")
                QTimer.singleShot(1500, lambda: self.login_success(pin))
        except Exception as e:
            self.show_error(f"Error: {str(e)}")
    
    def login_success(self, pin):
        """Handle successful login"""
        self.pin = pin
        self.show_success("Access granted! Unlocking your secure vault...")
        
        def open_dashboard():
            try:
                self.dashboard = Dashboard(pin)
                self.dashboard.show()
                self.close()
            except Exception as e:
                self.show_error(f"Failed to open vault: {str(e)}")
        
        QTimer.singleShot(1200, open_dashboard)
    
    def login_failed(self):
        """Handle failed login attempt"""
        self.failed_attempts += 1
        remaining = self.max_attempts - self.failed_attempts
        
        # Shake animation
        self.animator.shake_error(self.pin_input)
        
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
        self.pin_instruction.setText(message)
        self.pin_instruction.setStyleSheet("""
            font-size: 16px;
            font-weight: 600;
            color: #EF4444;
            margin: 10px 0;
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid #EF4444;
            border-radius: 8px;
            padding: 12px;
        """)
        
        # Clear after 4 seconds
        QTimer.singleShot(4000, self.restore_instruction)
    
    def show_success(self, message):
        """Show success message"""
        self.pin_instruction.setText(message)
        self.pin_instruction.setStyleSheet("""
            font-size: 16px;
            font-weight: 600;
            color: #10B981;
            margin: 10px 0;
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid #10B981;
            border-radius: 8px;
            padding: 12px;
        """)
    
    def restore_instruction(self):
        """Restore original instruction text"""
        instruction_text = "Set a secure PIN (4-6 digits)" if not pin_exists() else "Enter your PIN to unlock"
        self.pin_instruction.setText(instruction_text)
        self.pin_instruction.setStyleSheet("""
            font-size: 16px;
            font-weight: 500;
            color: #A1A1AA;
            margin: 10px 0;
        """)
    
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