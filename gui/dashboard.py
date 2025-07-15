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
        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(self.auto_save)
        
        self.setWindowTitle("Cryptex - Secure Vault")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)
        
        # Apply theme
        current_theme = settings.get("theme", "cyber_blue")
        self.setStyleSheet(generate_qss(current_theme))
        
        self.setup_ui()
        self.setup_menu()
        self.refresh_notes()
        self.center_window()
        
        # Start auto-save if enabled
        if settings.get("auto_save", True):
            interval = settings.get("auto_save_interval", 30) * 1000
            self.auto_save_timer.start(interval)
        
        # Animate window appearance
        animator.fade_in(self, 500)
    
    def setup_ui(self):
        """Setup the modern dashboard interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Left sidebar
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
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
        
        import_btn = QPushButton("📥")
        import_btn.setObjectName("SecondaryButton")
        import_btn.setToolTip("Import Vault")
        import_btn.clicked.connect(self.import_vault)
        io_layout.addWidget(import_btn)
        
        sidebar_layout.addLayout(io_layout)
        
        layout.addWidget(sidebar)
        
        # Main panel
        main_panel = QFrame()
        main_panel.setObjectName("MainPanel")
        main_layout = QVBoxLayout(main_panel)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # Title input
        title_layout = QHBoxLayout()
        title_layout.addWidget(QLabel("Title:"))
        
        self.note_title = QLineEdit()
        self.note_title.setPlaceholderText("Enter note title...")
        self.note_title.textChanged.connect(self.on_text_changed)
        title_layout.addWidget(self.note_title)
        
        # Word count label
        self.word_count_label = QLabel("0 words")
        self.word_count_label.setObjectName("InfoLabel")
        title_layout.addWidget(self.word_count_label)
        
        main_layout.addLayout(title_layout)
        
        # Content editor
        content_label = QLabel("Content:")
        content_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        main_layout.addWidget(content_label)
        
        self.note_text = QTextEdit()
        self.note_text.setPlaceholderText("Start writing your secure note here...\n\nYour notes are encrypted and stored locally for maximum security.")
        self.note_text.textChanged.connect(self.on_text_changed)
        main_layout.addWidget(self.note_text)
        
        # Status info
        self.status_label = QLabel("Ready")
        self.status_label.setObjectName("InfoLabel")
        main_layout.addWidget(self.status_label)
        
        layout.addWidget(main_panel)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
    
    def setup_menu(self):
        """Setup menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        new_action = QAction("New Note", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_note)
        file_menu.addAction(new_action)
        
        save_action = QAction("Save Note", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_note)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        export_action = QAction("Export Vault", self)
        export_action.triggered.connect(self.export_vault)
        file_menu.addAction(export_action)
        
        import_action = QAction("Import Vault", self)
        import_action.triggered.connect(self.import_vault)
        file_menu.addAction(import_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu("View")
        
        for theme_key, theme_data in THEMES.items():
            theme_action = QAction(theme_data["name"], self)
            theme_action.triggered.connect(lambda checked, t=theme_key: self.apply_theme(t))
            view_menu.addAction(theme_action)
    
    def center_window(self):
        """Center window on screen"""
        from PyQt6.QtWidgets import QApplication
        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )
    
    def apply_theme(self, theme_name):
        """Apply the selected theme"""
        self.setStyleSheet(generate_qss(theme_name))
        settings.set("theme", theme_name)
        
        # Update combo box
        for i in range(self.theme_combo.count()):
            if self.theme_combo.itemData(i) == theme_name:
                self.theme_combo.setCurrentIndex(i)
                break
        
        animator.pulse_widget(self.theme_combo)
    
    def on_theme_changed(self):
        """Handle theme change"""
        theme_key = self.theme_combo.currentData()
        if theme_key:
            self.apply_theme(theme_key)
    
    def refresh_notes(self):
        """Refresh the notes list"""
        self.note_list.clear()
        try:
            self.notes = load_data(self.pin)
            for title in sorted(self.notes.keys()):
                item = QListWidgetItem(title)
                self.note_list.addItem(item)
                
                # Animate item appearance
                animator.fade_in(item.listWidget(), 200)
        except Exception as e:
            print(f"Error loading notes: {e}")
            self.notes = {}
        
        # Update window title and status
        count = len(self.notes)
        if settings.get("show_note_count", True):
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
        # Stop auto-save timer
        self.auto_save_timer.stop()
        
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