from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QTextEdit, QLineEdit, 
                            QListWidget, QMessageBox, QSplitter, QFrame,
                            QToolBar, QStatusBar, QMenuBar, QMenu, QFileDialog,
                            QListWidgetItem, QGraphicsOpacityEffect, QSpacerItem, QSizePolicy)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QAction, QFont
from core.database import load_data, save_data, delete_note, export_vault, import_vault
from core.settings import settings
from assets.themes import generate_qss, THEMES
from datetime import datetime
import os

class Dashboard(QMainWindow):
    def __init__(self, pin):
        super().__init__()
        self.pin = pin
        self.current_note_title = None
        self.is_modified = False
        self.notes = {}
        self.animation = None
        
        self.setWindowTitle("Cryptex - Secure Notes")
        self.setMinimumSize(1000, 700)
        self.resize(1400, 900)
        
        # Apply theme
        self.apply_theme()
        
        # Setup UI
        self.setup_ui()
        self.setup_menu_bar()
        self.setup_toolbar()
        self.setup_status_bar()
        
        # Load data
        self.refresh_notes()
        
        # Center window and animate
        self.center_window()
        self.setup_animations()
    
    def apply_theme(self):
        """Apply current theme"""
        current_theme = settings.get("theme", "dark_modern")
        self.setStyleSheet(generate_qss(current_theme))
    
    def setup_animations(self):
        """Setup entrance animation"""
        self.opacity_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity_effect)
        
        self.fade_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_animation.setDuration(600)
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.fade_animation.start()
    
    def setup_ui(self):
        """Setup main UI with modern design"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Create splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #374151;
                width: 3px;
                border-radius: 1px;
            }
            QSplitter::handle:hover {
                background-color: #6366f1;
            }
        """)
        
        # Left panel (note list)
        self.setup_note_list_panel(splitter)
        
        # Right panel (note editor)
        self.setup_note_editor_panel(splitter)
        
        # Set splitter proportions
        splitter.setSizes([400, 800])
        
        main_layout.addWidget(splitter)
    
    def setup_note_list_panel(self, parent):
        """Setup modern note list panel"""
        panel = QFrame()
        panel.setObjectName("card")
        panel.setMaximumWidth(450)
        panel.setStyleSheet("""
            QFrame#card {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1a1a2e, stop:1 #16213e);
                border-radius: 20px;
                border: 2px solid #374151;
                padding: 25px;
            }
        """)
        layout = QVBoxLayout(panel)
        layout.setSpacing(20)
        
        # Header with modern styling
        header_layout = QVBoxLayout()
        header_layout.setSpacing(10)
        
        # Title and count
        title_layout = QHBoxLayout()
        
        notes_label = QLabel("📝 Your Notes")
        notes_label.setStyleSheet("""
            font-size: 24px;
            font-weight: 700;
            color: #ffffff;
            margin: 0;
        """)
        title_layout.addWidget(notes_label)
        
        title_layout.addStretch()
        
        self.note_count_label = QLabel()
        self.note_count_label.setStyleSheet("""
            background-color: #6366f1;
            color: white;
            padding: 6px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
        """)
        title_layout.addWidget(self.note_count_label)
        
        header_layout.addLayout(title_layout)
        
        # Subtitle
        subtitle = QLabel("Encrypted and secure")
        subtitle.setStyleSheet("""
            font-size: 14px;
            color: #a1a1aa;
            font-weight: 500;
            margin: 0;
        """)
        header_layout.addWidget(subtitle)
        
        layout.addLayout(header_layout)
        
        # Search box with modern styling
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search your notes...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 16px 20px;
                font-size: 15px;
                border-radius: 12px;
                background-color: #16213e;
                border: 2px solid #374151;
                color: #ffffff;
                font-weight: 500;
            }
            QLineEdit:focus {
                border: 2px solid #6366f1;
                background-color: #1a1a2e;
            }
            QLineEdit:hover {
                border: 2px solid #7c3aed;
            }
        """)
        self.search_input.textChanged.connect(self.filter_notes)
        layout.addWidget(self.search_input)
        
        # Note list with modern styling
        self.note_list = QListWidget()
        self.note_list.setStyleSheet("""
            QListWidget {
                background-color: #16213e;
                border: 2px solid #374151;
                border-radius: 16px;
                padding: 12px;
                outline: none;
            }
            QListWidget::item {
                background-color: transparent;
                color: #ffffff;
                padding: 16px 20px;
                border-radius: 12px;
                margin: 4px 0;
                border: 1px solid transparent;
                font-weight: 500;
                font-size: 15px;
            }
            QListWidget::item:hover {
                background-color: #1a1a2e;
                border: 1px solid #6366f1;
            }
            QListWidget::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6366f1, stop:1 #8b5cf6);
                color: white;
                font-weight: 600;
                border: 1px solid #a855f7;
            }
        """)
        self.note_list.itemClicked.connect(self.display_note)
        layout.addWidget(self.note_list)
        
        # Action buttons with modern styling
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(12)
        
        self.new_note_btn = QPushButton("✨ New Note")
        self.new_note_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6366f1, stop:1 #8b5cf6);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 14px 20px;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #7c3aed, stop:1 #a855f7);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4f46e5, stop:1 #7c2d12);
            }
        """)
        self.new_note_btn.clicked.connect(self.new_note)
        actions_layout.addWidget(self.new_note_btn)
        
        self.delete_btn = QPushButton("🗑️")
        self.delete_btn.setFixedSize(50, 50)
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #374151;
                color: #a1a1aa;
                border: none;
                border-radius: 12px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #ef4444;
                color: white;
            }
            QPushButton:disabled {
                background-color: #1f2937;
                color: #6b7280;
            }
        """)
        self.delete_btn.clicked.connect(self.delete_note)
        self.delete_btn.setEnabled(False)
        actions_layout.addWidget(self.delete_btn)
        
        layout.addLayout(actions_layout)
        parent.addWidget(panel)
    
    def setup_note_editor_panel(self, parent):
        """Setup modern note editor panel"""
        panel = QFrame()
        panel.setObjectName("card")
        panel.setStyleSheet("""
            QFrame#card {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1a1a2e, stop:1 #16213e);
                border-radius: 20px;
                border: 2px solid #374151;
                padding: 30px;
            }
        """)
        layout = QVBoxLayout(panel)
        layout.setSpacing(20)
        
        # Editor header
        editor_header = QHBoxLayout()
        editor_header.setSpacing(15)
        
        # Title input with modern styling
        self.note_title = QLineEdit()
        self.note_title.setPlaceholderText("✏️ Enter note title...")
        self.note_title.textChanged.connect(self.on_title_changed)
        self.note_title.setStyleSheet("""
            QLineEdit {
                font-size: 24px; 
                font-weight: 700; 
                padding: 20px 24px;
                border-radius: 16px;
                background-color: #16213e;
                border: 2px solid #374151;
                color: #ffffff;
            }
            QLineEdit:focus {
                border: 2px solid #6366f1;
                background-color: #1a1a2e;
            }
            QLineEdit:hover {
                border: 2px solid #7c3aed;
            }
        """)
        editor_header.addWidget(self.note_title)
        
        # Save button with modern styling
        self.save_btn = QPushButton("💾 Save")
        self.save_btn.setFixedSize(120, 60)
        self.save_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #10b981, stop:1 #059669);
                color: white;
                border: none;
                border-radius: 12px;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #059669, stop:1 #047857);
            }
            QPushButton:disabled {
                background-color: #374151;
                color: #6b7280;
            }
        """)
        self.save_btn.clicked.connect(self.save_note)
        self.save_btn.setEnabled(False)
        editor_header.addWidget(self.save_btn)
        
        layout.addLayout(editor_header)
        
        # Note content with modern styling
        self.note_text = QTextEdit()
        self.note_text.setPlaceholderText("📝 Start writing your secure note here...\n\nYour thoughts are encrypted and safe.")
        self.note_text.textChanged.connect(self.on_content_changed)
        self.note_text.setStyleSheet("""
            QTextEdit {
                background-color: #16213e;
                color: #ffffff;
                border: 2px solid #374151;
                border-radius: 16px;
                padding: 24px;
                font-size: 16px;
                font-weight: 500;
                line-height: 1.6;
                selection-background-color: #6366f1;
            }
            QTextEdit:focus {
                border: 2px solid #6366f1;
                background-color: #1a1a2e;
            }
        """)
        layout.addWidget(self.note_text)
        
        # Editor footer with stats
        footer_layout = QHBoxLayout()
        footer_layout.setSpacing(20)
        
        # Word count
        self.word_count_label = QLabel("Words: 0 | Characters: 0")
        self.word_count_label.setStyleSheet("""
            color: #a1a1aa; 
            font-size: 13px;
            font-weight: 500;
            padding: 8px 12px;
            background-color: #374151;
            border-radius: 8px;
        """)
        footer_layout.addWidget(self.word_count_label)
        
        footer_layout.addStretch()
        
        # Modified indicator
        self.modified_label = QLabel()
        self.modified_label.setStyleSheet("""
            color: #a1a1aa; 
            font-size: 13px;
            font-weight: 600;
            padding: 8px 12px;
            border-radius: 8px;
        """)
        footer_layout.addWidget(self.modified_label)
        
        layout.addLayout(footer_layout)
        parent.addWidget(panel)
    
    def setup_menu_bar(self):
        """Setup modern menu bar"""
        menubar = self.menuBar()
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: #1a1a2e;
                color: #ffffff;
                border-bottom: 2px solid #374151;
                padding: 8px;
                font-weight: 500;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 10px 16px;
                border-radius: 8px;
            }
            QMenuBar::item:selected {
                background-color: #6366f1;
                color: white;
            }
        """)
        
        # File menu
        file_menu = menubar.addMenu("📁 File")
        
        new_action = QAction("✨ New Note", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_note)
        file_menu.addAction(new_action)
        
        save_action = QAction("💾 Save Note", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_note)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        export_action = QAction("📤 Export Vault", self)
        export_action.triggered.connect(self.export_vault)
        file_menu.addAction(export_action)
        
        import_action = QAction("📥 Import Vault", self)
        import_action.triggered.connect(self.import_vault)
        file_menu.addAction(import_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("🚪 Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu("🎨 View")
        
        # Theme submenu
        theme_menu = view_menu.addMenu("🎭 Themes")
        for theme_key, theme_data in THEMES.items():
            action = QAction(theme_data["name"], self)
            action.triggered.connect(lambda checked, t=theme_key: self.change_theme(t))
            theme_menu.addAction(action)
        
        # Help menu
        help_menu = menubar.addMenu("❓ Help")
        
        about_action = QAction("ℹ️ About Cryptex", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def setup_toolbar(self):
        """Setup modern toolbar"""
        toolbar = self.addToolBar("Main")
        toolbar.setMovable(False)
        toolbar.setStyleSheet("""
            QToolBar {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1a1a2e, stop:1 #16213e);
                border: none;
                spacing: 8px;
                padding: 12px;
            }
            QToolBar QToolButton {
                background-color: transparent;
                color: #ffffff;
                border: none;
                padding: 12px 16px;
                border-radius: 10px;
                font-weight: 500;
                font-size: 14px;
            }
            QToolBar QToolButton:hover {
                background-color: #374151;
            }
            QToolBar QToolButton:pressed {
                background-color: #6366f1;
                color: white;
            }
        """)
        
        # Actions
        new_action = QAction("✨ New", self)
        new_action.triggered.connect(self.new_note)
        toolbar.addAction(new_action)
        
        save_action = QAction("💾 Save", self)
        save_action.triggered.connect(self.save_note)
        toolbar.addAction(save_action)
        
        toolbar.addSeparator()
        
        export_action = QAction("📤 Export", self)
        export_action.triggered.connect(self.export_vault)
        toolbar.addAction(export_action)
        
        import_action = QAction("📥 Import", self)
        import_action.triggered.connect(self.import_vault)
        toolbar.addAction(import_action)
    
    def setup_status_bar(self):
        """Setup modern status bar"""
        self.status_bar = self.statusBar()
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1a1a2e, stop:1 #16213e);
                color: #a1a1aa;
                border-top: 2px solid #374151;
                font-size: 12px;
                font-weight: 500;
                padding: 8px;
            }
        """)
        
        # Theme indicator
        theme_name = THEMES[settings.get("theme", "dark_modern")]["name"]
        self.theme_label = QLabel(f"🎨 {theme_name}")
        self.status_bar.addPermanentWidget(self.theme_label)

    def center_window(self):
        """Center window on screen"""
        screen = self.screen().availableGeometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )

    def refresh_notes(self):
        """Refresh the notes list with animation"""
        self.note_list.clear()
        try:
            self.notes = load_data(self.pin)
        except Exception as e:
            self.notes = {}
            print(f"Error loading notes: {e}")
        
        # Sort notes by title
        sorted_titles = sorted(self.notes.keys())
        
        for title in sorted_titles:
            item = QListWidgetItem(title)
            self.note_list.addItem(item)
        
        # Update note count with modern styling
        count = len(self.notes)
        self.note_count_label.setText(f"{count} notes")
        self.setWindowTitle(f"Cryptex - {count} secure notes")
    
    def filter_notes(self, text):
        """Filter notes based on search text"""
        for i in range(self.note_list.count()):
            item = self.note_list.item(i)
            if item:
                item.setHidden(text.lower() not in item.text().lower())

    def display_note(self, item):
        """Display selected note with error handling"""
        if not item:
            return
            
        # Save current note if modified
        if self.is_modified and self.current_note_title:
            self.save_note()
        
        try:
            title = item.text()
            if title in self.notes:
                self.current_note_title = title
                self.note_title.setText(title)
                self.note_text.setText(self.notes[title])
                self.is_modified = False
                self.update_ui_state()
                self.update_word_count()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to display note: {e}")
    
    def new_note(self):
        """Create a new note with animation"""
        # Save current note if modified
        if self.is_modified and self.current_note_title:
            self.save_note()
        
        # Clear editor with smooth transition
        self.note_title.clear()
        self.note_text.clear()
        self.current_note_title = None
        self.is_modified = False
        self.update_ui_state()
        
        # Focus title input
        self.note_title.setFocus()
        
        # Clear selection
        self.note_list.clearSelection()
        
        # Show success message
        self.status_bar.showMessage("✨ New note created", 2000)
    
    def on_title_changed(self):
        """Handle title change"""
        self.is_modified = True
        self.update_ui_state()
    
    def on_content_changed(self):
        """Handle content change"""
        self.is_modified = True
        self.update_ui_state()
        self.update_word_count()
    
    def update_word_count(self):
        """Update word and character count with modern styling"""
        text = self.note_text.toPlainText()
        words = len(text.split()) if text.strip() else 0
        chars = len(text)
        self.word_count_label.setText(f"📊 {words} words | {chars} characters")
    
    def update_ui_state(self):
        """Update UI state based on current note"""
        has_title = bool(self.note_title.text().strip())
        has_selection = bool(self.note_list.currentItem())
        
        self.save_btn.setEnabled(self.is_modified and has_title)
        self.delete_btn.setEnabled(has_selection)
        
        if self.is_modified:
            self.modified_label.setText("● Unsaved changes")
            self.modified_label.setStyleSheet("""
                color: #f59e0b; 
                font-size: 13px;
                font-weight: 600;
                padding: 8px 12px;
                background-color: rgba(245, 158, 11, 0.1);
                border: 1px solid #f59e0b;
                border-radius: 8px;
            """)
        else:
            self.modified_label.setText("✅ Saved")
            self.modified_label.setStyleSheet("""
                color: #10b981; 
                font-size: 13px;
                font-weight: 600;
                padding: 8px 12px;
                background-color: rgba(16, 185, 129, 0.1);
                border: 1px solid #10b981;
                border-radius: 8px;
            """)

    def save_note(self):
        """Save current note with feedback"""
        title = self.note_title.text().strip()
        text = self.note_text.toPlainText()
        
        if not title:
            QMessageBox.warning(self, "Missing Title", "Please enter a note title before saving.")
            self.note_title.setFocus()
            return
        
        try:
            save_data(self.pin, title, text)
            self.current_note_title = title
            self.is_modified = False
            self.refresh_notes()
            self.update_ui_state()
            
            # Show success message
            self.status_bar.showMessage(f"💾 '{title}' saved successfully", 3000)
            
            # Select the saved note in list
            for i in range(self.note_list.count()):
                item = self.note_list.item(i)
                if item and item.text() == title:
                    self.note_list.setCurrentRow(i)
                    break
                    
        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"Failed to save note: {e}")

    def delete_note(self):
        """Delete selected note with confirmation"""
        current_item = self.note_list.currentItem()
        if not current_item:
            QMessageBox.information(self, "No Selection", "Please select a note to delete.")
            return
        
        title = current_item.text()
        
        # Modern confirmation dialog
        reply = QMessageBox.question(
            self, "🗑️ Delete Note",
            f"Are you sure you want to delete '{title}'?\n\n"
            "⚠️ This action cannot be undone.",
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
            self.is_modified = False
            self.refresh_notes()
            self.update_ui_state()
            
            self.status_bar.showMessage(f"🗑️ '{title}' deleted", 3000)
            
        except Exception as e:
            QMessageBox.critical(self, "Delete Error", f"Failed to delete note: {e}")

    def export_vault(self):
        """Export vault to file"""
        default_name = f"cryptex_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.enc"
        path, _ = QFileDialog.getSaveFileName(
            self, "📤 Export Vault", default_name,
            "Cryptex Vault (*.enc);;All Files (*)"
        )
        if path:
            try:
                export_vault(path)
                QMessageBox.information(self, "✅ Export Successful", 
                                      f"Vault exported to:\n{path}")
                self.status_bar.showMessage("📤 Vault exported successfully", 3000)
            except Exception as e:
                QMessageBox.critical(self, "❌ Export Failed", f"Failed to export vault: {e}")

    def import_vault(self):
        """Import vault from file"""
        path, _ = QFileDialog.getOpenFileName(
            self, "📥 Import Vault", "",
            "Cryptex Vault (*.enc);;All Files (*)"
        )
        if path:
            reply = QMessageBox.question(
                self, "⚠️ Confirm Import",
                "Importing will replace your current vault.\n"
                "💡 Make sure you have a backup!\n\n"
                "Continue with import?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                try:
                    import_vault(path)
                    self.refresh_notes()
                    QMessageBox.information(self, "✅ Import Successful", 
                                          "Vault imported successfully!")
                    self.status_bar.showMessage("📥 Vault imported successfully", 3000)
                except Exception as e:
                    QMessageBox.critical(self, "❌ Import Failed", f"Failed to import vault: {e}")
    
    def change_theme(self, theme_key):
        """Change application theme with smooth transition"""
        settings.set("theme", theme_key)
        self.apply_theme()
        
        # Update status bar
        theme_name = THEMES[theme_key]["name"]
        self.theme_label.setText(f"🎨 {theme_name}")
        self.status_bar.showMessage(f"Theme changed to {theme_name}", 3000)
    
    def show_about(self):
        """Show modern about dialog"""
        QMessageBox.about(
            self, "About Cryptex",
            "<div style='text-align: center;'>"
            "<h2 style='color: #6366f1;'>🔐 Cryptex v2.0</h2>"
            "<p><b>Enhanced Secure Note Manager</b></p>"
            "<p>A modern, encrypted note-taking application with advanced security features.</p>"
            "<br>"
            "<p><b>🔒 Security Features:</b></p>"
            "<ul style='text-align: left;'>"
            "<li>🛡️ Military-grade AES encryption</li>"
            "<li>🔐 PIN-based authentication</li>"
            "<li>💾 Local storage only</li>"
            "<li>🚫 Zero data collection</li>"
            "</ul>"
            "<br>"
            "<p><b>🎨 Modern Features:</b></p>"
            "<ul style='text-align: left;'>"
            "<li>🌈 Multiple beautiful themes</li>"
            "<li>🔍 Real-time search</li>"
            "<li>📊 Word count & statistics</li>"
            "<li>💫 Smooth animations</li>"
            "</ul>"
            "<br>"
            "<p style='color: #a1a1aa;'><b>Created by:</b> Mrtn777<br>"
            "<b>Enhanced by:</b> Claude AI</p>"
            "</div>"
        )
    
    def closeEvent(self, event):
        """Handle window close event"""
        # Save current note if modified
        if self.is_modified and self.current_note_title:
            reply = QMessageBox.question(
                self, "💾 Unsaved Changes",
                "You have unsaved changes. Save before closing?",
                QMessageBox.StandardButton.Save | 
                QMessageBox.StandardButton.Discard | 
                QMessageBox.StandardButton.Cancel
            )
            
            if reply == QMessageBox.StandardButton.Save:
                self.save_note()
            elif reply == QMessageBox.StandardButton.Cancel:
                event.ignore()
                return
        
        event.accept()