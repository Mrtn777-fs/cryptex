"""Simple, clean dashboard that actually works"""
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QTextEdit, QLineEdit, 
                            QListWidget, QMessageBox, QSplitter, QFrame,
                            QFileDialog, QListWidgetItem)
from PyQt6.QtCore import Qt
from core.database import load_data, save_data, delete_note, export_vault, import_vault
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
        
        # Simple dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
                color: #ffffff;
            }
            QWidget {
                background-color: #1a1a1a;
                color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QFrame {
                background-color: #2a2a2a;
                border: 1px solid #444444;
                border-radius: 8px;
                padding: 15px;
            }
            QLabel {
                color: #ffffff;
            }
            QLineEdit, QTextEdit {
                background-color: #333333;
                border: 1px solid #00CFFF;
                border-radius: 6px;
                padding: 10px;
                color: white;
                font-size: 14px;
            }
            QLineEdit:focus, QTextEdit:focus {
                border-color: #66D9FF;
            }
            QPushButton {
                background-color: #00CFFF;
                color: #1a1a1a;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #66D9FF;
            }
            QPushButton:pressed {
                background-color: #0099CC;
            }
            QPushButton:disabled {
                background-color: #555555;
                color: #888888;
            }
            QListWidget {
                background-color: #2a2a2a;
                border: 1px solid #444444;
                border-radius: 6px;
                padding: 5px;
            }
            QListWidget::item {
                background-color: #333333;
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 10px;
                margin: 2px;
            }
            QListWidget::item:selected {
                background-color: #00CFFF;
                color: #1a1a1a;
            }
            QListWidget::item:hover {
                background-color: #444444;
            }
            QMenuBar {
                background-color: #2a2a2a;
                color: white;
                border-bottom: 1px solid #444444;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 8px 12px;
            }
            QMenuBar::item:selected {
                background-color: #00CFFF;
                color: #1a1a1a;
            }
            QMenu {
                background-color: #2a2a2a;
                border: 1px solid #444444;
                color: white;
            }
            QMenu::item {
                padding: 8px 20px;
            }
            QMenu::item:selected {
                background-color: #00CFFF;
                color: #1a1a1a;
            }
        """)
        
        self.setup_ui()
        self.setup_menu()
        self.refresh_notes()
        self.center_window()
    
    def setup_ui(self):
        """Setup simple, clean UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Left panel - Notes list
        left_panel = QFrame()
        left_panel.setFixedWidth(300)
        left_layout = QVBoxLayout(left_panel)
        
        # Header
        header = QLabel("📝 Your Notes")
        header.setStyleSheet("font-size: 18px; font-weight: bold; color: #00CFFF; margin-bottom: 10px;")
        left_layout.addWidget(header)
        
        # New note button
        new_btn = QPushButton("✨ New Note")
        new_btn.clicked.connect(self.new_note)
        left_layout.addWidget(new_btn)
        
        # Notes list
        self.note_list = QListWidget()
        self.note_list.itemClicked.connect(self.display_note)
        left_layout.addWidget(self.note_list)
        
        # Delete button
        self.delete_btn = QPushButton("🗑️ Delete Note")
        self.delete_btn.clicked.connect(self.delete_note)
        self.delete_btn.setEnabled(False)
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff4444;
                color: white;
            }
            QPushButton:hover {
                background-color: #ff6666;
            }
            QPushButton:disabled {
                background-color: #555555;
                color: #888888;
            }
        """)
        left_layout.addWidget(self.delete_btn)
        
        layout.addWidget(left_panel)
        
        # Right panel - Note editor
        right_panel = QFrame()
        right_layout = QVBoxLayout(right_panel)
        
        # Title input
        title_layout = QHBoxLayout()
        title_layout.addWidget(QLabel("Title:"))
        self.note_title = QLineEdit()
        self.note_title.setPlaceholderText("Enter note title...")
        title_layout.addWidget(self.note_title)
        
        self.save_btn = QPushButton("💾 Save")
        self.save_btn.clicked.connect(self.save_note)
        self.save_btn.setEnabled(False)
        title_layout.addWidget(self.save_btn)
        
        right_layout.addLayout(title_layout)
        
        # Content editor
        content_label = QLabel("Content:")
        right_layout.addWidget(content_label)
        
        self.note_text = QTextEdit()
        self.note_text.setPlaceholderText("Start writing your secure note here...")
        right_layout.addWidget(self.note_text)
        
        # Connect text change events
        self.note_title.textChanged.connect(self.on_text_changed)
        self.note_text.textChanged.connect(self.on_text_changed)
        
        layout.addWidget(right_panel)
    
    def setup_menu(self):
        """Setup menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        new_action = file_menu.addAction("New Note")
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_note)
        
        save_action = file_menu.addAction("Save Note")
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_note)
        
        file_menu.addSeparator()
        
        export_action = file_menu.addAction("Export Vault")
        export_action.triggered.connect(self.export_vault)
        
        import_action = file_menu.addAction("Import Vault")
        import_action.triggered.connect(self.import_vault)
        
        file_menu.addSeparator()
        
        exit_action = file_menu.addAction("Exit")
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
    
    def center_window(self):
        """Center window on screen"""
        from PyQt6.QtWidgets import QApplication
        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )
    
    def refresh_notes(self):
        """Refresh the notes list"""
        self.note_list.clear()
        try:
            self.notes = load_data(self.pin)
            for title in sorted(self.notes.keys()):
                self.note_list.addItem(title)
        except Exception as e:
            print(f"Error loading notes: {e}")
            self.notes = {}
        
        # Update window title
        count = len(self.notes)
        self.setWindowTitle(f"Cryptex - {count} notes")
    
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
    
    def new_note(self):
        """Create a new note"""
        self.note_title.clear()
        self.note_text.clear()
        self.current_note_title = None
        self.note_list.clearSelection()
        self.delete_btn.setEnabled(False)
        self.note_title.setFocus()
    
    def on_text_changed(self):
        """Handle text changes"""
        has_title = bool(self.note_title.text().strip())
        self.save_btn.setEnabled(has_title)
    
    def save_note(self):
        """Save current note"""
        title = self.note_title.text().strip()
        content = self.note_text.toPlainText()
        
        if not title:
            QMessageBox.warning(self, "Error", "Please enter a note title.")
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
            
            self.statusBar().showMessage(f"Note '{title}' saved successfully", 3000)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save note: {e}")
    
    def delete_note(self):
        """Delete selected note"""
        current_item = self.note_list.currentItem()
        if not current_item:
            return
        
        title = current_item.text()
        
        reply = QMessageBox.question(
            self, "Delete Note",
            f"Are you sure you want to delete '{title}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                delete_note(self.pin, title)
                self.note_title.clear()
                self.note_text.clear()
                self.current_note_title = None
                self.refresh_notes()
                self.delete_btn.setEnabled(False)
                self.statusBar().showMessage(f"Note '{title}' deleted", 3000)
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
                QMessageBox.information(self, "Success", f"Vault exported to:\n{path}")
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
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                try:
                    import_vault(path)
                    self.refresh_notes()
                    QMessageBox.information(self, "Success", "Vault imported successfully!")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to import vault: {e}")