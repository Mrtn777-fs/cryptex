"""
Clean dashboard for Cryptex
"""
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QTextEdit, QLineEdit, 
                            QListWidget, QMessageBox, QFrame,
                            QFileDialog, QListWidgetItem, QComboBox)
from PyQt6.QtCore import Qt
from core.database import load_data, save_data, delete_note, export_vault, import_vault
from assets.themes import THEMES, generate_qss
from core.settings import settings
from datetime import datetime

class Dashboard(QMainWindow):
    def __init__(self, pin):
        super().__init__()
        self.pin = pin
        self.current_note_title = None
        self.notes = {}
        
        self.setWindowTitle("Cryptex - Secure Vault")
        self.setMinimumSize(1000, 700)
        self.resize(1200, 800)
        
        # Apply theme
        current_theme = settings.get("theme", "cyber_blue")
        try:
            self.setStyleSheet(generate_qss(current_theme))
        except Exception as e:
            print(f"Theme error: {e}")
            # Fallback theme
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #1a1a1a;
                    color: white;
                }
                QPushButton {
                    background-color: #00CFFF;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 8px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #0099CC;
                }
                QLineEdit, QTextEdit {
                    background-color: #2a2a2a;
                    border: 1px solid #00CFFF;
                    border-radius: 6px;
                    padding: 8px;
                    color: white;
                }
                QListWidget {
                    background-color: #2a2a2a;
                    border: 1px solid #00CFFF;
                    border-radius: 6px;
                }
                QListWidget::item {
                    padding: 8px;
                    border-bottom: 1px solid #333;
                }
                QListWidget::item:selected {
                    background-color: #00CFFF;
                    color: white;
                }
            """)
        
        self.setup_ui()
        self.refresh_notes()
        self.center_window()
    
    def setup_ui(self):
        """Setup the dashboard interface"""
        try:
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            
            layout = QHBoxLayout(central_widget)
            layout.setContentsMargins(10, 10, 10, 10)
            layout.setSpacing(10)
            
            # Sidebar
            sidebar = QFrame()
            sidebar.setFixedWidth(300)
            sidebar_layout = QVBoxLayout(sidebar)
            sidebar_layout.setContentsMargins(15, 15, 15, 15)
            sidebar_layout.setSpacing(15)
            
            # Header
            header = QLabel("🔐 CRYPTEX")
            header.setStyleSheet("font-size: 24px; font-weight: bold; color: #00CFFF;")
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
            new_btn.clicked.connect(self.new_note)
            sidebar_layout.addWidget(new_btn)
            
            # Notes list
            self.note_list = QListWidget()
            self.note_list.itemClicked.connect(self.display_note)
            sidebar_layout.addWidget(self.note_list)
            
            # Action buttons
            self.save_btn = QPushButton("💾 Save")
            self.save_btn.clicked.connect(self.save_note)
            self.save_btn.setEnabled(False)
            sidebar_layout.addWidget(self.save_btn)
            
            self.delete_btn = QPushButton("🗑️ Delete")
            self.delete_btn.clicked.connect(self.delete_note)
            self.delete_btn.setEnabled(False)
            sidebar_layout.addWidget(self.delete_btn)
            
            # Export/Import buttons
            io_layout = QHBoxLayout()
            
            export_btn = QPushButton("📤 Export")
            export_btn.clicked.connect(self.export_vault)
            io_layout.addWidget(export_btn)
            
            import_btn = QPushButton("📥 Import")
            import_btn.clicked.connect(self.import_vault)
            io_layout.addWidget(import_btn)
            
            sidebar_layout.addLayout(io_layout)
            
            layout.addWidget(sidebar)
            
            # Main panel
            main_panel = QFrame()
            main_layout = QVBoxLayout(main_panel)
            main_layout.setContentsMargins(15, 15, 15, 15)
            main_layout.setSpacing(15)
            
            # Note title
            self.note_title = QLineEdit()
            self.note_title.setPlaceholderText("Note title...")
            self.note_title.textChanged.connect(self.on_text_changed)
            main_layout.addWidget(self.note_title)
            
            # Note content
            self.note_text = QTextEdit()
            self.note_text.setPlaceholderText("Start writing your secure note...")
            self.note_text.textChanged.connect(self.on_text_changed)
            main_layout.addWidget(self.note_text)
            
            layout.addWidget(main_panel)
        except Exception as e:
            print(f"UI setup error: {e}")
    
    def center_window(self):
        """Center window on screen"""
        try:
            from PyQt6.QtWidgets import QApplication
            screen = QApplication.primaryScreen().geometry()
            size = self.geometry()
            self.move(
                (screen.width() - size.width()) // 2,
                (screen.height() - size.height()) // 2
            )
        except Exception as e:
            print(f"Window centering error: {e}")
    
    def on_theme_changed(self):
        """Handle theme change"""
        try:
            theme_key = self.theme_combo.currentData()
            if theme_key:
                self.setStyleSheet(generate_qss(theme_key))
                settings.set("theme", theme_key)
        except Exception as e:
            print(f"Theme change error: {e}")
    
    def refresh_notes(self):
        """Refresh the notes list"""
        try:
            self.note_list.clear()
            self.notes = load_data(self.pin)
            for title in sorted(self.notes.keys()):
                item = QListWidgetItem(title)
                self.note_list.addItem(item)
            
            # Update window title
            count = len(self.notes)
            if count > 0:
                self.setWindowTitle(f"Cryptex - {count} notes")
            else:
                self.setWindowTitle("Cryptex - Secure Vault")
        except Exception as e:
            print(f"Error loading notes: {e}")
            self.notes = {}
    
    def display_note(self, item):
        """Display selected note"""
        try:
            if not item:
                return
            
            title = item.text()
            if title in self.notes:
                self.current_note_title = title
                self.note_title.setText(title)
                self.note_text.setText(self.notes[title])
                self.delete_btn.setEnabled(True)
        except Exception as e:
            print(f"Error displaying note: {e}")
    
    def new_note(self):
        """Create a new note"""
        try:
            self.note_title.clear()
            self.note_text.clear()
            self.current_note_title = None
            self.note_list.clearSelection()
            self.delete_btn.setEnabled(False)
            self.save_btn.setEnabled(False)
            self.note_title.setFocus()
        except Exception as e:
            print(f"Error creating new note: {e}")
    
    def on_text_changed(self):
        """Handle text changes"""
        try:
            has_title = bool(self.note_title.text().strip())
            self.save_btn.setEnabled(has_title)
        except Exception as e:
            print(f"Error handling text change: {e}")
    
    def save_note(self):
        """Save current note"""
        try:
            title = self.note_title.text().strip()
            content = self.note_text.toPlainText()
            
            if not title:
                QMessageBox.warning(self, "Error", "Please enter a note title.")
                return
            
            save_data(self.pin, title, content)
            self.current_note_title = title
            self.refresh_notes()
            
            # Select the saved note
            for i in range(self.note_list.count()):
                item = self.note_list.item(i)
                if item and item.text() == title:
                    self.note_list.setCurrentRow(i)
                    break
            
            QMessageBox.information(self, "Success", f"Note '{title}' saved successfully!")
        except Exception as e:
            print(f"Error saving note: {e}")
            QMessageBox.critical(self, "Error", f"Failed to save note: {e}")
    
    def delete_note(self):
        """Delete selected note"""
        try:
            current_item = self.note_list.currentItem()
            if not current_item:
                return
            
            title = current_item.text()
            
            reply = QMessageBox.question(
                self, "Delete Note",
                f"Are you sure you want to delete '{title}'?\n\nThis action cannot be undone.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply != QMessageBox.StandardButton.Yes:
                return
            
            delete_note(self.pin, title)
            self.note_title.clear()
            self.note_text.clear()
            self.current_note_title = None
            self.refresh_notes()
            self.delete_btn.setEnabled(False)
            self.save_btn.setEnabled(False)
            
            QMessageBox.information(self, "Success", f"Note '{title}' deleted successfully!")
        except Exception as e:
            print(f"Error deleting note: {e}")
            QMessageBox.critical(self, "Error", f"Failed to delete note: {e}")
    
    def export_vault(self):
        """Export vault to file"""
        try:
            default_name = f"cryptex_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.enc"
            path, _ = QFileDialog.getSaveFileName(
                self, "Export Vault", default_name,
                "Cryptex Vault (*.enc);;All Files (*)"
            )
            if path:
                export_vault(path)
                QMessageBox.information(self, "Success", f"Vault exported successfully to:\n{path}")
        except Exception as e:
            print(f"Error exporting vault: {e}")
            QMessageBox.critical(self, "Error", f"Failed to export vault: {e}")
    
    def import_vault(self):
        """Import vault from file"""
        try:
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
                    import_vault(path)
                    self.refresh_notes()
                    self.new_note()
                    QMessageBox.information(self, "Success", "Vault imported successfully!")
        except Exception as e:
            print(f"Error importing vault: {e}")
            QMessageBox.critical(self, "Error", f"Failed to import vault: {e}")
    
    def keyPressEvent(self, event):
        """Handle key press events"""
        try:
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
        except Exception as e:
            print(f"Key press error: {e}")
    
    def closeEvent(self, event):
        """Handle close event"""
        event.accept()