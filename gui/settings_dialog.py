"""Settings dialog for Cryptex"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QComboBox, QCheckBox, QSpinBox,
                            QTabWidget, QWidget, QGroupBox, QSlider,
                            QMessageBox, QLineEdit, QFormLayout)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from core.settings import settings
from core.auth import change_pin, get_auth_config, save_auth_config
from assets.themes import THEMES, generate_qss
from gui.animations import animator

class SettingsDialog(QDialog):
    theme_changed = pyqtSignal(str)
    settings_changed = pyqtSignal()
    
    def __init__(self, current_pin, parent=None):
        super().__init__(parent)
        self.current_pin = current_pin
        self.setWindowTitle("Cryptex Settings")
        self.setFixedSize(500, 600)
        self.setModal(True)
        
        # Apply current theme
        current_theme = settings.get("theme", "dark_red")
        self.setStyleSheet(generate_qss(current_theme))
        
        self.setup_ui()
        self.load_current_settings()
        
        # Animate dialog appearance
        animator.fade_in(self, 200)
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Settings")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Tab widget
        self.tabs = QTabWidget()
        
        # Appearance tab
        self.setup_appearance_tab()
        
        # Security tab
        self.setup_security_tab()
        
        # General tab
        self.setup_general_tab()
        
        # Advanced tab
        self.setup_advanced_tab()
        
        layout.addWidget(self.tabs)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.reset_btn = QPushButton("Reset to Defaults")
        self.cancel_btn = QPushButton("Cancel")
        self.apply_btn = QPushButton("Apply")
        self.ok_btn = QPushButton("OK")
        
        self.reset_btn.clicked.connect(self.reset_settings)
        self.cancel_btn.clicked.connect(self.reject)
        self.apply_btn.clicked.connect(self.apply_settings)
        self.ok_btn.clicked.connect(self.accept_settings)
        
        button_layout.addWidget(self.reset_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.apply_btn)
        button_layout.addWidget(self.ok_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def setup_appearance_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Theme selection
        theme_group = QGroupBox("Theme")
        theme_layout = QFormLayout()
        
        self.theme_combo = QComboBox()
        for theme_key, theme_data in THEMES.items():
            self.theme_combo.addItem(theme_data["name"], theme_key)
        self.theme_combo.currentTextChanged.connect(self.preview_theme)
        
        theme_layout.addRow("Theme:", self.theme_combo)
        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)
        
        # Font settings
        font_group = QGroupBox("Font")
        font_layout = QFormLayout()
        
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(10, 24)
        self.font_size_spin.setSuffix(" px")
        
        font_layout.addRow("Font Size:", self.font_size_spin)
        font_group.setLayout(font_layout)
        layout.addWidget(font_group)
        
        layout.addStretch()
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Appearance")
    
    def setup_security_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        # PIN settings
        pin_group = QGroupBox("PIN Settings")
        pin_layout = QVBoxLayout()
        
        # Change PIN
        change_pin_layout = QHBoxLayout()
        self.change_pin_btn = QPushButton("Change PIN")
        self.change_pin_btn.clicked.connect(self.change_pin_dialog)
        change_pin_layout.addWidget(QLabel("Change your PIN:"))
        change_pin_layout.addStretch()
        change_pin_layout.addWidget(self.change_pin_btn)
        pin_layout.addLayout(change_pin_layout)
        
        # Session timeout
        timeout_layout = QHBoxLayout()
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(0, 120)
        self.timeout_spin.setSuffix(" min")
        self.timeout_spin.setSpecialValueText("No timeout")
        timeout_layout.addWidget(QLabel("Session timeout:"))
        timeout_layout.addStretch()
        timeout_layout.addWidget(self.timeout_spin)
        pin_layout.addLayout(timeout_layout)
        
        pin_group.setLayout(pin_layout)
        layout.addWidget(pin_group)
        
        # Backup settings
        backup_group = QGroupBox("Backup & Security")
        backup_layout = QVBoxLayout()
        
        self.backup_on_exit_cb = QCheckBox("Create backup on exit")
        self.confirm_delete_cb = QCheckBox("Confirm before deleting notes")
        
        backup_layout.addWidget(self.backup_on_exit_cb)
        backup_layout.addWidget(self.confirm_delete_cb)
        
        backup_group.setLayout(backup_layout)
        layout.addWidget(backup_group)
        
        layout.addStretch()
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Security")
    
    def setup_general_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Auto-save settings
        autosave_group = QGroupBox("Auto-save")
        autosave_layout = QVBoxLayout()
        
        self.auto_save_cb = QCheckBox("Enable auto-save")
        autosave_layout.addWidget(self.auto_save_cb)
        
        interval_layout = QHBoxLayout()
        self.autosave_interval_spin = QSpinBox()
        self.autosave_interval_spin.setRange(5, 300)
        self.autosave_interval_spin.setSuffix(" seconds")
        interval_layout.addWidget(QLabel("Auto-save interval:"))
        interval_layout.addStretch()
        interval_layout.addWidget(self.autosave_interval_spin)
        autosave_layout.addLayout(interval_layout)
        
        autosave_group.setLayout(autosave_layout)
        layout.addWidget(autosave_group)
        
        # UI settings
        ui_group = QGroupBox("User Interface")
        ui_layout = QVBoxLayout()
        
        self.show_welcome_cb = QCheckBox("Show welcome message")
        self.show_note_count_cb = QCheckBox("Show note count in title")
        
        ui_layout.addWidget(self.show_welcome_cb)
        ui_layout.addWidget(self.show_note_count_cb)
        
        ui_group.setLayout(ui_layout)
        layout.addWidget(ui_group)
        
        layout.addStretch()
        tab.setLayout(layout)
        self.tabs.addTab(tab, "General")
    
    def setup_advanced_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Advanced settings
        advanced_group = QGroupBox("Advanced")
        advanced_layout = QVBoxLayout()
        
        # Data location
        data_layout = QHBoxLayout()
        data_layout.addWidget(QLabel("Data folder: data/"))
        open_folder_btn = QPushButton("Open Folder")
        open_folder_btn.clicked.connect(self.open_data_folder)
        data_layout.addStretch()
        data_layout.addWidget(open_folder_btn)
        advanced_layout.addLayout(data_layout)
        
        # Reset all data
        reset_layout = QHBoxLayout()
        reset_data_btn = QPushButton("Reset All Data")
        reset_data_btn.setStyleSheet("QPushButton { background-color: #d32f2f; }")
        reset_data_btn.clicked.connect(self.reset_all_data)
        reset_layout.addWidget(QLabel("Danger Zone:"))
        reset_layout.addStretch()
        reset_layout.addWidget(reset_data_btn)
        advanced_layout.addLayout(reset_layout)
        
        advanced_group.setLayout(advanced_layout)
        layout.addWidget(advanced_group)
        
        layout.addStretch()
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Advanced")
    
    def load_current_settings(self):
        """Load current settings into UI"""
        # Theme
        current_theme = settings.get("theme", "dark_red")
        for i in range(self.theme_combo.count()):
            if self.theme_combo.itemData(i) == current_theme:
                self.theme_combo.setCurrentIndex(i)
                break
        
        # Font size
        self.font_size_spin.setValue(settings.get("font_size", 14))
        
        # Auto-save
        self.auto_save_cb.setChecked(settings.get("auto_save", True))
        self.autosave_interval_spin.setValue(settings.get("auto_save_interval", 30))
        
        # UI settings
        self.show_welcome_cb.setChecked(settings.get("show_welcome", True))
        self.show_note_count_cb.setChecked(settings.get("show_note_count", True))
        
        # Security
        self.timeout_spin.setValue(settings.get("session_timeout", 0))
        self.backup_on_exit_cb.setChecked(settings.get("backup_on_exit", False))
        self.confirm_delete_cb.setChecked(settings.get("confirm_delete", True))
    
    def preview_theme(self):
        """Preview theme change"""
        theme_key = self.theme_combo.currentData()
        if theme_key:
            self.setStyleSheet(generate_qss(theme_key))
            self.theme_changed.emit(theme_key)
    
    def change_pin_dialog(self):
        """Show change PIN dialog"""
        dialog = ChangePinDialog(self.current_pin, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.current_pin = dialog.new_pin
            QMessageBox.information(self, "Success", "PIN changed successfully!")
    
    def open_data_folder(self):
        """Open data folder in file explorer"""
        import subprocess
        import platform
        
        try:
            if platform.system() == "Windows":
                subprocess.run(["explorer", "data"])
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", "data"])
            else:  # Linux
                subprocess.run(["xdg-open", "data"])
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not open folder: {e}")
    
    def reset_all_data(self):
        """Reset all application data"""
        reply = QMessageBox.question(
            self, "Reset All Data",
            "This will delete ALL your notes, settings, and PIN.\n"
            "This action cannot be undone!\n\n"
            "Are you sure you want to continue?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            import shutil
            try:
                shutil.rmtree("data")
                QMessageBox.information(self, "Reset Complete", 
                                      "All data has been reset. Please restart the application.")
                self.accept()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to reset data: {e}")
    
    def apply_settings(self):
        """Apply settings without closing dialog"""
        self.save_settings()
        self.settings_changed.emit()
    
    def accept_settings(self):
        """Apply settings and close dialog"""
        self.save_settings()
        self.settings_changed.emit()
        self.accept()
    
    def save_settings(self):
        """Save all settings"""
        # Theme
        theme_key = self.theme_combo.currentData()
        settings.set("theme", theme_key)
        
        # Font
        settings.set("font_size", self.font_size_spin.value())
        
        # Auto-save
        settings.set("auto_save", self.auto_save_cb.isChecked())
        settings.set("auto_save_interval", self.autosave_interval_spin.value())
        
        # UI
        settings.set("show_welcome", self.show_welcome_cb.isChecked())
        settings.set("show_note_count", self.show_note_count_cb.isChecked())
        
        # Security
        settings.set("session_timeout", self.timeout_spin.value())
        settings.set("backup_on_exit", self.backup_on_exit_cb.isChecked())
        settings.set("confirm_delete", self.confirm_delete_cb.isChecked())
    
    def reset_settings(self):
        """Reset all settings to defaults"""
        reply = QMessageBox.question(
            self, "Reset Settings",
            "Reset all settings to default values?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            settings.reset_to_defaults()
            self.load_current_settings()
            self.settings_changed.emit()

class ChangePinDialog(QDialog):
    def __init__(self, current_pin, parent=None):
        super().__init__(parent)
        self.current_pin = current_pin
        self.new_pin = None
        
        self.setWindowTitle("Change PIN")
        self.setFixedSize(300, 200)
        self.setModal(True)
        
        layout = QVBoxLayout()
        
        # Current PIN
        layout.addWidget(QLabel("Current PIN:"))
        self.current_pin_input = QLineEdit()
        self.current_pin_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.current_pin_input)
        
        # New PIN
        layout.addWidget(QLabel("New PIN:"))
        self.new_pin_input = QLineEdit()
        self.new_pin_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.new_pin_input)
        
        # Confirm PIN
        layout.addWidget(QLabel("Confirm New PIN:"))
        self.confirm_pin_input = QLineEdit()
        self.confirm_pin_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.confirm_pin_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        cancel_btn = QPushButton("Cancel")
        change_btn = QPushButton("Change PIN")
        
        cancel_btn.clicked.connect(self.reject)
        change_btn.clicked.connect(self.change_pin)
        
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(change_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def change_pin(self):
        current = self.current_pin_input.text()
        new = self.new_pin_input.text()
        confirm = self.confirm_pin_input.text()
        
        if current != self.current_pin:
            QMessageBox.warning(self, "Error", "Current PIN is incorrect")
            animator.shake(self.current_pin_input)
            return
        
        if len(new) < 4:
            QMessageBox.warning(self, "Error", "PIN must be at least 4 characters")
            animator.shake(self.new_pin_input)
            return
        
        if new != confirm:
            QMessageBox.warning(self, "Error", "New PINs do not match")
            animator.shake(self.confirm_pin_input)
            return
        
        if change_pin(current, new):
            self.new_pin = new
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "Failed to change PIN")