"""Modern glassmorphism dashboard for Cryptex"""
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QTextEdit, QLineEdit, 
                            QListWidget, QMessageBox, QSplitter, QFrame,
                            QMenuBar, QFileDialog,
                            QListWidgetItem, QScrollArea, QGridLayout, QSpacerItem, QSizePolicy)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPropertyAnimation, QEasingCurve, QSize
from PyQt6.QtGui import QAction, QFont, QIcon
from core.database import load_data, save_data, delete_note, export_vault, import_vault
from core.settings import settings
from assets.themes import get_modern_qss, COLORS
from gui.animations import ModernAnimator
from datetime import datetime
import os

class Dashboard(QMainWindow):
    def __init__(self, pin):
        super().__init__()
        self.pin = pin
        self.animator = ModernAnimator()
        self.current_note_title = None
        self.is_modified = False
        self.notes = {}
        self.current_view = "notes"
        
        self.setWindowTitle("Cryptex - Secure Vault")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)
        
        # Apply modern theme
        self.setStyleSheet(get_modern_qss())
        
        # Setup UI
        self.setup_ui()
        self.setup_menu_bar()
        self.setup_status_bar()
        
        # Load data
        self.refresh_notes()
        
        # Center window and animate
        self.center_window()
        self.animator.fade_in(self, 600)
    
    def setup_ui(self):
        """Setup modern glassmorphism dashboard UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Sidebar
        self.setup_sidebar(main_layout)
        
        # Main content area
        self.setup_main_content(main_layout)
    
    def setup_sidebar(self, parent_layout):
        """Setup modern sidebar with navigation"""
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(280)
        sidebar.setStyleSheet(f"""
            QFrame#sidebar {{
                background: rgba(26, 26, 46, 0.9);
                border: 1px solid rgba(0, 207, 255, 0.2);
                border-radius: 20px;
                padding: 20px;
            }}
        """)
        
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setSpacing(20)
        
        # Sidebar header
        header = QLabel("🔐 CRYPTEX")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet(f"""
            font-size: 24px;
            font-weight: 700;
            color: {COLORS['primary']};
            margin: 10px 0 20px 0;
        """)
        sidebar_layout.addWidget(header)
        
        # Navigation buttons
        nav_buttons = [
            ("📝", "Notes", "notes"),
            ("🔑", "Passwords", "passwords"),
            ("📁", "Vaults", "vaults"),
            ("⚙️", "Settings", "settings")
        ]
        
        self.nav_buttons = {}
        for icon, text, view_id in nav_buttons:
            btn = QPushButton(f"{icon} {text}")
            btn.setStyleSheet(self.get_nav_button_style(view_id == "notes"))
            btn.clicked.connect(lambda checked, v=view_id: self.switch_view(v))
            btn.setFixedHeight(50)
            self.nav_buttons[view_id] = btn
            sidebar_layout.addWidget(btn)
        
        sidebar_layout.addStretch()
        
        # Vault stats
        stats_frame = QFrame()
        stats_frame.setStyleSheet(f"""
            background: rgba(0, 207, 255, 0.1);
            border: 1px solid rgba(0, 207, 255, 0.3);
            border-radius: 12px;
            padding: 15px;
        """)
        stats_layout = QVBoxLayout(stats_frame)
        
        self.stats_label = QLabel("📊 Vault Statistics")
        self.stats_label.setStyleSheet(f"""
            font-size: 14px;
            font-weight: 600;
            color: {COLORS['primary']};
            margin-bottom: 8px;
        """)
        stats_layout.addWidget(self.stats_label)
        
        self.note_count_label = QLabel("0 notes stored")
        self.note_count_label.setStyleSheet(f"""
            font-size: 12px;
            color: {COLORS['text_secondary']};
        """)
        stats_layout.addWidget(self.note_count_label)
        
        sidebar_layout.addWidget(stats_frame)
        
        parent_layout.addWidget(sidebar)
    
    def setup_main_content(self, parent_layout):
        """Setup main content area"""
        # Create stacked content area
        self.content_stack = QWidget()
        content_layout = QVBoxLayout(self.content_stack)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Notes view (default)
        self.notes_view = self.create_notes_view()
        content_layout.addWidget(self.notes_view)
        
        parent_layout.addWidget(self.content_stack)
    
    def create_notes_view(self):
        """Create the notes view with modern card layout"""
        notes_widget = QWidget()
        layout = QVBoxLayout(notes_widget)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("📝 Your Secure Notes")
        title.setStyleSheet(f"""
            font-size: 28px;
            font-weight: 700;
            color: {COLORS['text']};
        """)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # New note button
        new_note_btn = QPushButton("✨ New Note")
        new_note_btn.setObjectName("primary")
        new_note_btn.clicked.connect(self.new_note)
        new_note_btn.setFixedHeight(45)
        header_layout.addWidget(new_note_btn)
        
        layout.addLayout(header_layout)
        
        # Search bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search your notes...")
        self.search_input.setStyleSheet(f"""
            QLineEdit {{
                background: rgba(26, 26, 46, 0.6);
                border: 2px solid rgba(0, 207, 255, 0.3);
                border-radius: 12px;
                padding: 12px 16px;
                font-size: 14px;
                color: {COLORS['text']};
            }}
            QLineEdit:focus {{
                border: 2px solid {COLORS['primary']};
                background: rgba(26, 26, 46, 0.8);
            }}
        """)
        self.search_input.textChanged.connect(self.filter_notes)
        search_layout.addWidget(self.search_input)
        
        layout.addLayout(search_layout)
        
        # Notes content area
        content_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Notes list
        self.setup_notes_list(content_splitter)
        
        # Note editor
        self.setup_note_editor(content_splitter)
        
        content_splitter.setSizes([400, 800])
        layout.addWidget(content_splitter)
        
        return notes_widget
    
    def setup_notes_list(self, parent):
        """Setup notes list with modern cards"""
        list_frame = QFrame()
        list_frame.setStyleSheet(f"""
            QFrame {{
                background: rgba(26, 26, 46, 0.6);
                border: 1px solid rgba(0, 207, 255, 0.2);
                border-radius: 16px;
                padding: 20px;
            }}
        """)
        list_layout = QVBoxLayout(list_frame)
        
        # List header
        list_header = QLabel("📋 All Notes")
        list_header.setStyleSheet(f"""
            font-size: 18px;
            font-weight: 600;
            color: {COLORS['text']};
            margin-bottom: 15px;
        """)
        list_layout.addWidget(list_header)
        
        # Notes list
        self.note_list = QListWidget()
        self.note_list.itemClicked.connect(self.display_note)
        list_layout.addWidget(self.note_list)
        
        # Delete button
        self.delete_btn = QPushButton("🗑️ Delete Note")
        self.delete_btn.setStyleSheet(f"""
            QPushButton {{
                background: rgba(239, 68, 68, 0.8);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-weight: 600;
                margin-top: 10px;
            }}
            QPushButton:hover {{
                background: rgba(239, 68, 68, 1.0);
            }}
            QPushButton:disabled {{
                background: rgba(107, 114, 128, 0.5);
                color: rgba(255, 255, 255, 0.5);
            }}
        """)
        self.delete_btn.clicked.connect(self.delete_note)
        self.delete_btn.setEnabled(False)
        list_layout.addWidget(self.delete_btn)
        
        parent.addWidget(list_frame)
    
    def setup_note_editor(self, parent):
        """Setup note editor with modern styling"""
        editor_frame = QFrame()
        editor_frame.setStyleSheet(f"""
            QFrame {{
                background: rgba(26, 26, 46, 0.6);
                border: 1px solid rgba(0, 207, 255, 0.2);
                border-radius: 16px;
                padding: 25px;
            }}
        """)
        editor_layout = QVBoxLayout(editor_frame)
        editor_layout.setSpacing(20)
        
        # Editor header
        header_layout = QHBoxLayout()
        
        # Title input
        self.note_title = QLineEdit()
        self.note_title.setPlaceholderText("✏️ Enter note title...")
        self.note_title.textChanged.connect(self.on_title_changed)
        self.note_title.setStyleSheet(f"""
            QLineEdit {{
                font-size: 20px;
                font-weight: 600;
                padding: 15px 20px;
                border-radius: 12px;
                background: rgba(26, 26, 46, 0.8);
                border: 2px solid rgba(0, 207, 255, 0.3);
                color: {COLORS['text']};
            }}
            QLineEdit:focus {{
                border: 2px solid {COLORS['primary']};
            }}
        """)
        header_layout.addWidget(self.note_title)
        
        # Save button
        self.save_btn = QPushButton("💾 Save")
        self.save_btn.setObjectName("primary")
        self.save_btn.clicked.connect(self.save_note)
        self.save_btn.setEnabled(False)
        self.save_btn.setFixedSize(100, 50)
        header_layout.addWidget(self.save_btn)
        
        editor_layout.addLayout(header_layout)
        
        # Note content
        self.note_text = QTextEdit()
        self.note_text.setPlaceholderText("📝 Start writing your secure note here...\n\nYour thoughts are encrypted and protected.")
        self.note_text.textChanged.connect(self.on_content_changed)
        editor_layout.addWidget(self.note_text)
        
        # Editor footer
        footer_layout = QHBoxLayout()
        
        self.word_count_label = QLabel("Words: 0 | Characters: 0")
        self.word_count_label.setStyleSheet(f"""
            color: {COLORS['text_secondary']};
            font-size: 12px;
            padding: 8px 12px;
            background: rgba(0, 207, 255, 0.1);
            border-radius: 6px;
        """)
        footer_layout.addWidget(self.word_count_label)
        
        footer_layout.addStretch()
        
        self.modified_label = QLabel("✅ Saved")
        self.modified_label.setStyleSheet(f"""
            color: {COLORS['success']};
            font-size: 12px;
            font-weight: 600;
            padding: 8px 12px;
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid {COLORS['success']};
            border-radius: 6px;
        """)
        footer_layout.addWidget(self.modified_label)
        
        editor_layout.addLayout(footer_layout)
        
        parent.addWidget(editor_frame)
    
    def get_nav_button_style(self, active=False):
        """Get navigation button style"""
        if active:
            return f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 {COLORS['primary']}, stop:1 {COLORS['secondary']});
                    color: white;
                    border: none;
                    border-radius: 12px;
                    padding: 12px 16px;
                    font-size: 14px;
                    font-weight: 600;
                    text-align: left;
                }}
            """
        else:
            return f"""
                QPushButton {{
                    background: rgba(26, 26, 46, 0.5);
                    color: {COLORS['text_secondary']};
                    border: 1px solid rgba(0, 207, 255, 0.2);
                    border-radius: 12px;
                    padding: 12px 16px;
                    font-size: 14px;
                    font-weight: 500;
                    text-align: left;
                }}
                QPushButton:hover {{
                    background: rgba(0, 207, 255, 0.1);
                    color: {COLORS['primary']};
                    border: 1px solid rgba(0, 207, 255, 0.4);
                }}
            """
    
    def setup_menu_bar(self):
        """Setup modern menu bar"""
        menubar = self.menuBar()
        
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
        
        # Help menu
        help_menu = menubar.addMenu("❓ Help")
        
        about_action = QAction("ℹ️ About Cryptex", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def setup_status_bar(self):
        """Setup modern status bar"""
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("🔐 Vault unlocked and ready")
    
    def center_window(self):
        """Center window on screen"""
        screen = self.screen().availableGeometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )
    
    def switch_view(self, view_id):
        """Switch between different views"""
        # Update navigation buttons
        for btn_id, btn in self.nav_buttons.items():
            btn.setStyleSheet(self.get_nav_button_style(btn_id == view_id))
        
        self.current_view = view_id
        
        if view_id == "notes":
            # Already showing notes view
            pass
        elif view_id == "passwords":
            self.status_bar.showMessage("🔑 Passwords feature coming soon...")
        elif view_id == "vaults":
            self.status_bar.showMessage("📁 Vaults feature coming soon...")
        elif view_id == "settings":
            self.status_bar.showMessage("⚙️ Settings feature coming soon...")
    
    def refresh_notes(self):
        """Refresh the notes list"""
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
        
        # Update stats
        count = len(self.notes)
        self.note_count_label.setText(f"{count} notes stored")
        self.setWindowTitle(f"Cryptex - {count} secure notes")
    
    def filter_notes(self, text):
        """Filter notes based on search text"""
        for i in range(self.note_list.count()):
            item = self.note_list.item(i)
            if item:
                item.setHidden(text.lower() not in item.text().lower())
    
    def display_note(self, item):
        """Display selected note"""
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
        """Create a new note"""
        # Save current note if modified
        if self.is_modified and self.current_note_title:
            self.save_note()
        
        # Clear editor
        self.note_title.clear()
        self.note_text.clear()
        self.current_note_title = None
        self.is_modified = False
        self.update_ui_state()
        
        # Focus title input
        self.note_title.setFocus()
        
        # Clear selection
        self.note_list.clearSelection()
        
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
        """Update word and character count"""
        text = self.note_text.toPlainText()
        words = len(text.split()) if text.strip() else 0
        chars = len(text)
        self.word_count_label.setText(f"Words: {words} | Characters: {chars}")
    
    def update_ui_state(self):
        """Update UI state based on current note"""
        has_title = bool(self.note_title.text().strip())
        has_selection = bool(self.note_list.currentItem())
        
        self.save_btn.setEnabled(self.is_modified and has_title)
        self.delete_btn.setEnabled(has_selection)
        
        if self.is_modified:
            self.modified_label.setText("● Unsaved changes")
            self.modified_label.setStyleSheet(f"""
                color: {COLORS['warning']};
                font-size: 12px;
                font-weight: 600;
                padding: 8px 12px;
                background: rgba(245, 158, 11, 0.1);
                border: 1px solid {COLORS['warning']};
                border-radius: 6px;
            """)
        else:
            self.modified_label.setText("✅ Saved")
            self.modified_label.setStyleSheet(f"""
                color: {COLORS['success']};
                font-size: 12px;
                font-weight: 600;
                padding: 8px 12px;
                background: rgba(16, 185, 129, 0.1);
                border: 1px solid {COLORS['success']};
                border-radius: 6px;
            """)
    
    def save_note(self):
        """Save current note"""
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
        """Delete selected note"""
        current_item = self.note_list.currentItem()
        if not current_item:
            QMessageBox.information(self, "No Selection", "Please select a note to delete.")
            return
        
        title = current_item.text()
        
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
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self, "About Cryptex",
            f"""
            <div style='text-align: center;'>
            <h2 style='color: {COLORS['primary']};'>🔐 Cryptex v2.0</h2>
            <p><b>Modern Secure Note Manager</b></p>
            <p>A beautiful, encrypted note-taking application with glassmorphism design.</p>
            <br>
            <p><b>🔒 Security Features:</b></p>
            <ul style='text-align: left;'>
            <li>🛡️ Military-grade AES encryption</li>
            <li>🔐 PIN-based authentication</li>
            <li>💾 Local storage only</li>
            <li>🚫 Zero data collection</li>
            </ul>
            <br>
            <p style='color: {COLORS['text_secondary']};'><b>Created by:</b> Mrtn777<br>
            <b>Enhanced with:</b> Modern UI Design</p>
            </div>
            """
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