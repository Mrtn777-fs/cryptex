"""
Modern dashboard for Cryptex with smooth animations
"""
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QTextEdit, QLineEdit, 
                            QListWidget, QMessageBox, QSplitter, QFrame,
                            QFileDialog, QListWidgetItem, QStatusBar,
                            QComboBox, QSpacerItem, QSizePolicy)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QAction
from core.database import load_data, save_data, delete_note, export_vault, import_vault
from assets.themes import THEMES, generate_qss
from gui.animations import animator
from core.settings import settings
from datetime import datetime

class Dashboard(QMainWindow):
    def __init__(self, pin):
        super().__init__()
        self.pin = pin
        self.current_note_title = None
        self.notes = {}
        
        self.setWindowTitle("Cryptex - Secure Vault")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)
        
        try:
            # Apply theme
            current_theme = settings.get("theme", "cyber_blue")
            self.setStyleSheet(generate_qss(current_theme))
        except Exception as e:
            print(f"Theme error: {e}")
            # Fallback to basic dark theme
            self.setStyleSheet("QWidget { background-color: #1e1e1e; color: white; }")
        
        self.setup_ui()
        try:
            self.setup_ui()
            self.refresh_notes()
            self.center_window()
        except Exception as e:
            print(f"Dashboard setup error: {e}")
        
        # Start auto-save if enabled
        if settings.get("auto_save", True):
            interval = settings.get("auto_save_interval", 30) * 1000
            self.auto_save_timer.start(interval)
        
        # Animate window appearance
        animator.fade_in(self, 500)
    
    def setup_ui(self):
        """Setup the modern dashboard interface"""
        try:
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            
            layout = QHBoxLayout(central_widget)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)
            
            # Create sidebar and main panel
            self.create_sidebar(layout)
            self.create_main_panel(layout)
        except Exception as e:
            print(f"UI setup error: {e}")
        sidebar.setFixedWidth(300)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(20, 20, 20, 20)
        sidebar_layout.setSpacing(20)
        
        # Header
        header = QLabel("📝 Your Secure Notes")
        header.setObjectName("Title")
        header.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 10px;")
        sidebar_layout.addWidget(header)
        
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
        
        sidebar_layout.addLayout(theme_layout)
        
        # New note button
        new_btn = QPushButton("✨ New Note")
        new_btn.setObjectName("PrimaryButton")
        new_btn.clicked.connect(self.new_note)
        sidebar_layout.addWidget(new_btn)
        
        # Notes list
        self.note_list = QListWidget()
        self.note_list.itemClicked.connect(self.display_note)
        sidebar_layout.addWidget(self.note_list)
        
        # Action buttons
        button_layout = QVBoxLayout()
        button_layout.setSpacing(10)
        
        self.save_btn = QPushButton("💾 Save Note")
        self.save_btn.setObjectName("PrimaryButton")
        self.save_btn.clicked.connect(self.save_note)
        self.save_btn.setEnabled(False)
        button_layout.addWidget(self.save_btn)
        
        self.delete_btn = QPushButton("🗑️ Delete Note")
        self.delete_btn.setObjectName("SecondaryButton")
        self.delete_btn.clicked.connect(self.delete_note)
        self.delete_btn.setEnabled(False)
        self.delete_btn.setStyleSheet("""
            QPushButton#SecondaryButton {
                border-color: #ff4444;
                color: #ff4444;
            }
            QPushButton#SecondaryButton:hover {
                background-color: #ff4444;
                color: white;
            }
        """)
        button_layout.addWidget(self.delete_btn)
        
        sidebar_layout.addLayout(button_layout)
        
        # Export/Import buttons
        io_layout = QHBoxLayout()
        
        export_btn = QPushButton("📤")
        export_btn.setObjectName("SecondaryButton")
        export_btn.setToolTip("Export Vault")
        export_btn.clicked.connect(self.export_vault)
        io_layout.addWidget(export_btn)
        
        try:
            sidebar = QFrame()
            sidebar.setFixedWidth(280)
            sidebar.setStyleSheet("""
                QFrame {
                    background: rgba(30, 30, 30, 0.95);
                    border-right: 2px solid rgba(0, 207, 255, 0.3);
                }
            """)
            
            sidebar_layout = QVBoxLayout(sidebar)
            sidebar_layout.setContentsMargins(20, 20, 20, 20)
            sidebar_layout.setSpacing(20)
            
            # Header
            header = QLabel("🔐 CRYPTEX")
            header.setStyleSheet("font-size: 24px; font-weight: bold; color: #00CFFF; margin-bottom: 10px;")
            sidebar_layout.addWidget(header)
            
            # Theme selector
            theme_layout = QHBoxLayout()
            theme_layout.addWidget(QLabel("Theme:"))
            
            self.theme_combo = QComboBox()
            for theme_key, theme_data in THEMES.items():
                self.theme_combo.addItem(theme_data["name"], theme_key)
            
            current_theme = settings.get("theme", "cyber_blue")
            for i in range(self.theme_combo.count()):
                if self.theme_combo.itemData(i) == current_theme:
                    self.theme_combo.setCurrentIndex(i)
                    break
            
            self.theme_combo.currentTextChanged.connect(self.on_theme_changed)
            theme_layout.addWidget(self.theme_combo)
            sidebar_layout.addLayout(theme_layout)
            
            # New note button
            new_btn = QPushButton("✨ New Note")
            new_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #00CFFF, stop:1 #0099CC);
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 12px;
                    font-weight: bold;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background: #00CFFF;
                }
            """)
            new_btn.clicked.connect(self.new_note)
            sidebar_layout.addWidget(new_btn)
            
            # Notes list
            self.note_list = QListWidget()
            self.note_list.setStyleSheet("""
                QListWidget {
                    background: rgba(40, 40, 40, 0.8);
                    border: 1px solid rgba(0, 207, 255, 0.3);
                    border-radius: 8px;
                    padding: 5px;
                }
                QListWidget::item {
                    background: rgba(50, 50, 50, 0.8);
                    border: 1px solid rgba(0, 207, 255, 0.2);
                    border-radius: 6px;
                    padding: 10px;
                    margin: 2px;
                    color: white;
                }
                QListWidget::item:selected {
                    background: rgba(0, 207, 255, 0.3);
                    border-color: #00CFFF;
                }
                QListWidget::item:hover {
                    background: rgba(0, 207, 255, 0.2);
                }
            """)
            self.note_list.itemClicked.connect(self.display_note)
            sidebar_layout.addWidget(self.note_list)
            
            # Action buttons
            self.save_btn = QPushButton("💾 Save")
            self.save_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #00CFFF, stop:1 #0099CC);
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 8px;
                    font-weight: bold;
                }
                QPushButton:hover { background: #00CFFF; }
                QPushButton:disabled { background: #555; color: #999; }
            """)
            self.save_btn.clicked.connect(self.save_note)
            self.save_btn.setEnabled(False)
            sidebar_layout.addWidget(self.save_btn)
            
            self.delete_btn = QPushButton("🗑️ Delete")
            self.delete_btn.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    color: #ff4444;
                    border: 2px solid #ff4444;
                    border-radius: 6px;
                    padding: 8px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: #ff4444;
                    color: white;
                }
                QPushButton:disabled { border-color: #555; color: #999; }
            """)
            self.delete_btn.clicked.connect(self.delete_note)
            self.delete_btn.setEnabled(False)
            sidebar_layout.addWidget(self.delete_btn)
            
            sidebar_layout.addStretch()
            parent_layout.addWidget(sidebar)
        except Exception as e:
            print(f"Sidebar creation error: {e}")
    
    def refresh_notes(self):
        """Refresh the notes list"""
        try:
            self.note_list.clear()
            self.notes = load_data(self.pin)
            for title in sorted(self.notes.keys()):
                item = QListWidgetItem(title)
                self.note_list.addItem(item)
                
                # Animate item appearance
                animator.fade_in(item.listWidget(), 200)
        except Exception as e:
            print(f"Error loading notes: {e}")
            self.notes = {}
        try:
            theme_key = self.theme_combo.currentData()
            if theme_key:
                self.setStyleSheet(generate_qss(theme_key))
                settings.set("theme", theme_key)
        except Exception as e:
            print(f"Theme change error: {e}")
            self.setWindowTitle(f"Cryptex - {count} notes")
        else:
            self.setWindowTitle("Cryptex - Secure Vault")
        
        self.status_bar.showMessage(f"{count} notes in vault")
    
    def display_note(self, item):
        """Display selected note"""
        if not item:
            return
        
        title = item.text()
        if title in self.notes:
            self.current_note_title = title
            self.note_title.setText(title)
            self.note_text.setText(self.notes[title])
            self.delete_btn.setEnabled(True)
            
            # Update word count
            self.update_word_count()
            
            # Animate note loading
            animator.pulse_widget(self.note_title)
    
    def new_note(self):
        """Create a new note"""
        self.note_title.clear()
        self.note_text.clear()
        self.current_note_title = None
        self.note_list.clearSelection()
        self.delete_btn.setEnabled(False)
        self.save_btn.setEnabled(False)
        self.note_title.setFocus()
        
        # Update status
        self.status_label.setText("New note")
        self.update_word_count()
        
        # Animate new note
        animator.pulse_widget(self.note_title)
    
    def on_text_changed(self):
        """Handle text changes"""
        has_title = bool(self.note_title.text().strip())
        has_content = bool(self.note_text.toPlainText().strip())
        
        self.save_btn.setEnabled(has_title)
        
        # Update word count
        self.update_word_count()
        
        # Update status
        if has_title or has_content:
            self.status_label.setText("Modified")
        else:
            self.status_label.setText("Ready")
    
    def update_word_count(self):
        """Update word count display"""
        content = self.note_text.toPlainText()
        word_count = len(content.split()) if content.strip() else 0
        char_count = len(content)
        
        self.word_count_label.setText(f"{word_count} words, {char_count} chars")
    
    def auto_save(self):
        """Auto-save current note if enabled"""
        if not settings.get("auto_save", True):
            return
        
        title = self.note_title.text().strip()
        content = self.note_text.toPlainText()
        
        if title and content and self.current_note_title == title:
            try:
                save_data(self.pin, title, content)
                self.status_label.setText("Auto-saved")
                QTimer.singleShot(2000, lambda: self.status_label.setText("Ready"))
            except Exception as e:
                print(f"Auto-save failed: {e}")
    
    def save_note(self):
        """Save current note"""
        title = self.note_title.text().strip()
        content = self.note_text.toPlainText()
        
        if not title:
            QMessageBox.warning(self, "Error", "Please enter a note title.")
            animator.shake_widget(self.note_title)
            return
        
        try:
            save_data(self.pin, title, content)
            self.current_note_title = title
            self.refresh_notes()
            
            # Select the saved note
            for i in range(self.note_list.count()):
                item = self.note_list.item(i)
                if item and item.text() == title:
                    self.note_list.setCurrentRow(i)
                    break
            
            # Success feedback
            self.status_label.setText("Saved successfully")
            self.status_bar.showMessage(f"Note '{title}' saved successfully", 3000)
            animator.pulse_widget(self.save_btn)
            
            QTimer.singleShot(2000, lambda: self.status_label.setText("Ready"))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save note: {e}")
    
    def delete_note(self):
        """Delete selected note"""
        current_item = self.note_list.currentItem()
        if not current_item:
            return
        
        title = current_item.text()
        
        if settings.get("confirm_delete", True):
            reply = QMessageBox.question(
                self, "Delete Note",
                f"Are you sure you want to delete '{title}'?\n\nThis action cannot be undone.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply != QMessageBox.StandardButton.Yes:
                return
        
        try:
            delete_note(self.pin, title)
            self.note_title.clear()
            self.note_text.clear()
            self.current_note_title = None
            self.refresh_notes()
            self.delete_btn.setEnabled(False)
            self.save_btn.setEnabled(False)
            
            # Success feedback
            self.status_label.setText("Note deleted")
            self.status_bar.showMessage(f"Note '{title}' deleted", 3000)
            self.update_word_count()
            
            QTimer.singleShot(2000, lambda: self.status_label.setText("Ready"))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete note: {e}")
    
    def export_vault(self):
        """Export vault to file"""
        default_name = f"cryptex_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.enc"
        path, _ = QFileDialog.getSaveFileName(
            self, "Export Vault", default_name,
            "Cryptex Vault (*.enc);;All Files (*)"
        )
        if path:
            try:
                export_vault(path)
                QMessageBox.information(self, "Success", f"Vault exported successfully to:\n{path}")
                self.status_bar.showMessage("Vault exported successfully", 3000)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export vault: {e}")
    
    def import_vault(self):
        """Import vault from file"""
        path, _ = QFileDialog.getOpenFileName(
            self, "Import Vault", "",
            "Cryptex Vault (*.enc);;All Files (*)"
        )
        if path:
            reply = QMessageBox.question(
                self, "Confirm Import",
                "Importing will replace your current vault.\n"
                "Make sure you have a backup!\n\n"
                "Continue?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                try:
                    import_vault(path)
                    self.refresh_notes()
                    self.new_note()  # Clear current note
                    QMessageBox.information(self, "Success", "Vault imported successfully!")
                    self.status_bar.showMessage("Vault imported successfully", 3000)
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to import vault: {e}")
    
    def keyPressEvent(self, event):
        """Handle key press events"""
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        elif event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if event.key() == Qt.Key.Key_N:
                self.new_note()
            elif event.key() == Qt.Key.Key_S:
                self.save_note()
            elif event.key() == Qt.Key.Key_Q:
                self.close()
        super().keyPressEvent(event)
    
    def closeEvent(self, event):
        """Handle close event"""
        # Optional backup on exit
        if settings.get("backup_on_exit", False):
            try:
                backup_name = f"data/auto_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.enc"
                export_vault(backup_name)
            except Exception as e:
                print(f"Auto-backup failed: {e}")
        
        # Fade out animation
        fade_animation = animator.fade_out(self, 300)
        fade_animation.finished.connect(lambda: event.accept())
        
        # Force close after animation timeout
        QTimer.singleShot(400, lambda: event.accept())