@@ .. @@
-from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QLineEdit, QListWidget, QMessageBox, QHBoxLayout
+from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
+                            QLabel, QPushButton, QTextEdit, QLineEdit, 
+                            QListWidget, QMessageBox, QSplitter, QFrame,
+                            QToolBar, QStatusBar, QMenuBar, QMenu, QFileDialog,
+                            QProgressBar, QSystemTrayIcon, QApplication,
+                            QListWidgetItem, QTextBrowser, QTabWidget)
+from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QThread, pyqtSlot
+from PyQt6.QtGui import QAction, QIcon, QFont, QTextCharFormat, QColor, QPixmap
 from core.database import load_data, save_data, delete_note, export_vault, import_vault
-from PyQt6.QtWidgets import QFileDialog
+from core.settings import settings
+from assets.themes import generate_qss, THEMES
+from gui.animations import animator
+from gui.settings_dialog import SettingsDialog
+import os
+import json
+from datetime import datetime

-class Dashboard(QWidget):
+class AutoSaveThread(QThread):
+    """Background thread for auto-saving"""
+    save_requested = pyqtSignal(str, str, str)  # pin, title, content
+    
+    def __init__(self):
+        super().__init__()
+        self.pin = None
+        self.title = None
+        self.content = None
+        self.should_save = False
+    
+    def set_data(self, pin, title, content):
+        self.pin = pin
+        self.title = title
+        self.content = content
+        self.should_save = True
+    
+    def run(self):
+        if self.should_save and self.pin and self.title:
+            save_data(self.pin, self.title, self.content)
+            self.should_save = False

+class Dashboard(QMainWindow):
     def __init__(self, pin):
         super().__init__()
         self.pin = pin
+        self.current_note_title = None
+        self.is_modified = False
+        self.notes = {}
+        
         self.setWindowTitle("Cryptex")
-        self.setFixedSize(600, 500)
-        self.setStyleSheet(open("assets/dark.qss").read())
+        self.setMinimumSize(900, 600)
+        self.resize(1200, 800)
+        
+        # Apply theme
+        self.apply_theme()
+        
+        # Setup auto-save
+        self.setup_autosave()
+        
+        # Setup UI
+        self.setup_ui()
+        self.setup_menu_bar()
+        self.setup_toolbar()
+        self.setup_status_bar()
+        
+        # Load data
+        self.refresh_notes()
+        
+        # Center window
+        self.center_window()
+        
+        # Animate appearance
+        animator.fade_in(self, 300)
+        
+        # Load window geometry
+        self.load_geometry()
+    
+    def apply_theme(self):
+        """Apply current theme"""
+        current_theme = settings.get("theme", "dark_red")
+        self.setStyleSheet(generate_qss(current_theme))
+    
+    def setup_autosave(self):
+        """Setup auto-save functionality"""
+        self.autosave_thread = AutoSaveThread()
+        self.autosave_thread.save_requested.connect(self.on_autosave_complete)
+        
+        self.autosave_timer = QTimer()
+        self.autosave_timer.timeout.connect(self.autosave_current_note)
+        
+        if settings.get("auto_save", True):
+            interval = settings.get("auto_save_interval", 30) * 1000
+            self.autosave_timer.start(interval)
+    
+    def setup_ui(self):
+        """Setup main UI"""
+        central_widget = QWidget()
+        self.setCentralWidget(central_widget)
+        
+        # Main layout
+        main_layout = QHBoxLayout(central_widget)
+        main_layout.setContentsMargins(10, 10, 10, 10)
+        
+        # Create splitter
+        splitter = QSplitter(Qt.Orientation.Horizontal)
+        
+        # Left panel (note list)
+        self.setup_note_list_panel(splitter)
+        
+        # Right panel (note editor)
+        self.setup_note_editor_panel(splitter)
+        
+        # Set splitter proportions
+        splitter.setSizes([300, 600])
+        splitter.setStretchFactor(0, 0)
+        splitter.setStretchFactor(1, 1)
+        
+        main_layout.addWidget(splitter)
+    
+    def setup_note_list_panel(self, parent):
+        """Setup note list panel"""
+        panel = QFrame()
+        panel.setObjectName("card")
+        panel.setMaximumWidth(350)
+        layout = QVBoxLayout(panel)
+        
+        # Header
+        header_layout = QHBoxLayout()
+        
+        notes_label = QLabel("📝 Your Notes")
+        notes_label.setObjectName("subtitle")
+        header_layout.addWidget(notes_label)
+        
+        self.note_count_label = QLabel()
+        self.note_count_label.setStyleSheet("color: #888; font-size: 12px;")
+        header_layout.addStretch()
+        header_layout.addWidget(self.note_count_label)
+        
+        layout.addLayout(header_layout)
+        
+        # Search box
+        self.search_input = QLineEdit()
+        self.search_input.setPlaceholderText("🔍 Search notes...")
+        self.search_input.textChanged.connect(self.filter_notes)
+        layout.addWidget(self.search_input)
+        
+        # Note list
+        self.note_list = QListWidget()
+        self.note_list.itemClicked.connect(self.display_note)
+        self.note_list.setAlternatingRowColors(True)
+        layout.addWidget(self.note_list)
+        
+        # Quick actions
+        actions_layout = QHBoxLayout()
+        
+        self.new_note_btn = QPushButton("+ New")
+        self.new_note_btn.clicked.connect(self.new_note)
+        actions_layout.addWidget(self.new_note_btn)
+        
+        self.delete_btn = QPushButton("🗑️")
+        self.delete_btn.setMaximumWidth(40)
+        self.delete_btn.clicked.connect(self.delete_note)
+        self.delete_btn.setEnabled(False)
+        actions_layout.addWidget(self.delete_btn)
+        
+        layout.addLayout(actions_layout)
+        parent.addWidget(panel)
+    
+    def setup_note_editor_panel(self, parent):
+        """Setup note editor panel"""
+        panel = QFrame()
+        panel.setObjectName("card")
+        layout = QVBoxLayout(panel)
+        
+        # Editor header
+        editor_header = QHBoxLayout()
+        
+        # Title input
+        self.note_title = QLineEdit()
+        self.note_title.setPlaceholderText("Note title...")
+        self.note_title.textChanged.connect(self.on_title_changed)
+        self.note_title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 12px;")
+        editor_header.addWidget(self.note_title)
+        
+        # Save button
+        self.save_btn = QPushButton("💾 Save")
+        self.save_btn.clicked.connect(self.save_note)
+        self.save_btn.setEnabled(False)
+        editor_header.addWidget(self.save_btn)
+        
+        layout.addLayout(editor_header)
+        
+        # Note content
+        self.note_text = QTextEdit()
+        self.note_text.setPlaceholderText("Start writing your note here...")
+        self.note_text.textChanged.connect(self.on_content_changed)
+        layout.addWidget(self.note_text)
+        
+        # Editor footer
+        footer_layout = QHBoxLayout()
+        
+        self.word_count_label = QLabel("Words: 0 | Characters: 0")
+        self.word_count_label.setStyleSheet("color: #888; font-size: 12px;")
+        footer_layout.addWidget(self.word_count_label)
+        
+        footer_layout.addStretch()
+        
+        self.modified_label = QLabel()
+        self.modified_label.setStyleSheet("color: #888; font-size: 12px;")
+        footer_layout.addWidget(self.modified_label)
+        
+        layout.addLayout(footer_layout)
+        parent.addWidget(panel)
+    
+    def setup_menu_bar(self):
+        """Setup menu bar"""
+        menubar = self.menuBar()
+        
+        # File menu
+        file_menu = menubar.addMenu("File")
+        
+        new_action = QAction("New Note", self)
+        new_action.setShortcut("Ctrl+N")
+        new_action.triggered.connect(self.new_note)
+        file_menu.addAction(new_action)
+        
+        save_action = QAction("Save Note", self)
+        save_action.setShortcut("Ctrl+S")
+        save_action.triggered.connect(self.save_note)
+        file_menu.addAction(save_action)
+        
+        file_menu.addSeparator()
+        
+        export_action = QAction("Export Vault", self)
+        export_action.triggered.connect(self.export_vault)
+        file_menu.addAction(export_action)
+        
+        import_action = QAction("Import Vault", self)
+        import_action.triggered.connect(self.import_vault)
+        file_menu.addAction(import_action)
+        
+        file_menu.addSeparator()
+        
+        exit_action = QAction("Exit", self)
+        exit_action.setShortcut("Ctrl+Q")
+        exit_action.triggered.connect(self.close)
+        file_menu.addAction(exit_action)
+        
+        # Edit menu
+        edit_menu = menubar.addMenu("Edit")
+        
+        find_action = QAction("Find", self)
+        find_action.setShortcut("Ctrl+F")
+        find_action.triggered.connect(self.focus_search)
+        edit_menu.addAction(find_action)
+        
+        delete_action = QAction("Delete Note", self)
+        delete_action.setShortcut("Delete")
+        delete_action.triggered.connect(self.delete_note)
+        edit_menu.addAction(delete_action)
+        
+        # View menu
+        view_menu = menubar.addMenu("View")
+        
+        # Theme submenu
+        theme_menu = view_menu.addMenu("Theme")
+        for theme_key, theme_data in THEMES.items():
+            action = QAction(theme_data["name"], self)
+            action.triggered.connect(lambda checked, t=theme_key: self.change_theme(t))
+            theme_menu.addAction(action)
+        
+        # Tools menu
+        tools_menu = menubar.addMenu("Tools")
+        
+        settings_action = QAction("Settings", self)
+        settings_action.setShortcut("Ctrl+,")
+        settings_action.triggered.connect(self.open_settings)
+        tools_menu.addAction(settings_action)
+        
+        # Help menu
+        help_menu = menubar.addMenu("Help")
+        
+        about_action = QAction("About", self)
+        about_action.triggered.connect(self.show_about)
+        help_menu.addAction(about_action)
+    
+    def setup_toolbar(self):
+        """Setup toolbar"""
+        toolbar = self.addToolBar("Main")
+        toolbar.setMovable(False)
+        
+        # New note
+        new_action = QAction("📝 New", self)
+        new_action.triggered.connect(self.new_note)
+        toolbar.addAction(new_action)
+        
+        # Save
+        save_action = QAction("💾 Save", self)
+        save_action.triggered.connect(self.save_note)
+        toolbar.addAction(save_action)
+        
+        toolbar.addSeparator()
+        
+        # Export/Import
+        export_action = QAction("📤 Export", self)
+        export_action.triggered.connect(self.export_vault)
+        toolbar.addAction(export_action)
+        
+        import_action = QAction("📥 Import", self)
+        import_action.triggered.connect(self.import_vault)
+        toolbar.addAction(import_action)
+        
+        toolbar.addSeparator()
+        
+        # Settings
+        settings_action = QAction("⚙️ Settings", self)
+        settings_action.triggered.connect(self.open_settings)
+        toolbar.addAction(settings_action)
+    
+    def setup_status_bar(self):
+        """Setup status bar"""
+        self.status_bar = self.statusBar()
+        
+        # Auto-save indicator
+        self.autosave_label = QLabel("Auto-save: ON" if settings.get("auto_save") else "Auto-save: OFF")
+        self.status_bar.addPermanentWidget(self.autosave_label)
+        
+        # Theme indicator
+        theme_name = THEMES[settings.get("theme", "dark_red")]["name"]
+        self.theme_label = QLabel(f"Theme: {theme_name}")
+        self.status_bar.addPermanentWidget(self.theme_label)

-        layout = QVBoxLayout()
-
-        self.note_list = QListWidget()
-        self.note_list.itemClicked.connect(self.display_note)
-
-        self.note_title = QLineEdit()
-        self.note_title.setPlaceholderText("Title")
-
-        self.note_text = QTextEdit()
-        self.save_btn = QPushButton("Save Note")
-        self.del_btn = QPushButton("Delete Note")
-        self.exp_btn = QPushButton("Export Vault")
-        self.imp_btn = QPushButton("Import Vault")
-
-        self.save_btn.clicked.connect(self.save_note)
-        self.del_btn.clicked.connect(self.delete_note)
-        self.exp_btn.clicked.connect(self.export_vault)
-        self.imp_btn.clicked.connect(self.import_vault)
-
-        layout.addWidget(QLabel("Your Cryptex Notes"))
-        layout.addWidget(self.note_list)
-        layout.addWidget(self.note_title)
-        layout.addWidget(self.note_text)
-
-        btn_layout = QHBoxLayout()
-        btn_layout.addWidget(self.save_btn)
-        btn_layout.addWidget(self.del_btn)
-        btn_layout.addWidget(self.exp_btn)
-        btn_layout.addWidget(self.imp_btn)
-        layout.addLayout(btn_layout)
-
-        self.setLayout(layout)
-        self.refresh_notes()
+    def center_window(self):
+        """Center window on screen"""
+        screen = self.screen().availableGeometry()
+        size = self.geometry()
+        self.move(
+            (screen.width() - size.width()) // 2,
+            (screen.height() - size.height()) // 2
+        )
+    
+    def load_geometry(self):
+        """Load saved window geometry"""
+        geometry = settings.get("window_geometry")
+        if geometry:
+            self.restoreGeometry(geometry)
+    
+    def save_geometry(self):
+        """Save window geometry"""
+        settings.set("window_geometry", self.saveGeometry())

     def refresh_notes(self):
         self.note_list.clear()
         self.notes = load_data(self.pin)
-        for title in self.notes:
-            self.note_list.addItem(title)
+        
+        # Sort notes by title
+        sorted_titles = sorted(self.notes.keys())
+        
+        for title in sorted_titles:
+            item = QListWidgetItem(title)
+            item.setToolTip(f"Created: {title}")  # You could store creation date
+            self.note_list.addItem(item)
+        
+        # Update note count
+        count = len(self.notes)
+        if settings.get("show_note_count", True):
+            self.note_count_label.setText(f"({count})")
+            self.setWindowTitle(f"Cryptex - {count} notes")
+        else:
+            self.note_count_label.setText("")
+            self.setWindowTitle("Cryptex")
+    
+    def filter_notes(self, text):
+        """Filter notes based on search text"""
+        for i in range(self.note_list.count()):
+            item = self.note_list.item(i)
+            item.setHidden(text.lower() not in item.text().lower())

     def display_note(self, item):
+        # Save current note if modified
+        if self.is_modified and self.current_note_title:
+            self.save_note()
+        
         title = item.text()
+        self.current_note_title = title
         self.note_title.setText(title)
         self.note_text.setText(self.notes[title])
+        self.is_modified = False
+        self.update_ui_state()
+        self.update_word_count()
+        
+        # Animate note loading
+        animator.fade_in(self.note_text, 200)
+    
+    def new_note(self):
+        """Create a new note"""
+        # Save current note if modified
+        if self.is_modified and self.current_note_title:
+            self.save_note()
+        
+        # Clear editor
+        self.note_title.clear()
+        self.note_text.clear()
+        self.current_note_title = None
+        self.is_modified = False
+        self.update_ui_state()
+        
+        # Focus title input
+        self.note_title.setFocus()
+        
+        # Clear selection
+        self.note_list.clearSelection()
+    
+    def on_title_changed(self):
+        """Handle title change"""
+        self.is_modified = True
+        self.update_ui_state()
+    
+    def on_content_changed(self):
+        """Handle content change"""
+        self.is_modified = True
+        self.update_ui_state()
+        self.update_word_count()
+    
+    def update_word_count(self):
+        """Update word and character count"""
+        text = self.note_text.toPlainText()
+        words = len(text.split()) if text.strip() else 0
+        chars = len(text)
+        self.word_count_label.setText(f"Words: {words} | Characters: {chars}")
+    
+    def update_ui_state(self):
+        """Update UI state based on current note"""
+        has_title = bool(self.note_title.text().strip())
+        has_selection = bool(self.note_list.currentItem())
+        
+        self.save_btn.setEnabled(self.is_modified and has_title)
+        self.delete_btn.setEnabled(has_selection)
+        
+        if self.is_modified:
+            self.modified_label.setText("● Modified")
+            self.modified_label.setStyleSheet("color: #ff6666; font-size: 12px;")
+        else:
+            self.modified_label.setText("Saved")
+            self.modified_label.setStyleSheet("color: #66ff66; font-size: 12px;")

     def save_note(self):
         title = self.note_title.text()
         text = self.note_text.toPlainText()
-        if title:
+        
+        if not title.strip():
+            QMessageBox.warning(self, "Error", "Please enter a note title")
+            self.note_title.setFocus()
+            animator.shake(self.note_title)
+            return
+        
+        try:
             save_data(self.pin, title, text)
+            self.current_note_title = title
+            self.is_modified = False
             self.refresh_notes()
+            self.update_ui_state()
+            
+            # Show success message in status bar
+            self.status_bar.showMessage(f"Note '{title}' saved successfully", 3000)
+            
+            # Select the saved note in list
+            for i in range(self.note_list.count()):
+                if self.note_list.item(i).text() == title:
+                    self.note_list.setCurrentRow(i)
+                    break
+                    
+        except Exception as e:
+            QMessageBox.critical(self, "Error", f"Failed to save note: {e}")
+    
+    def autosave_current_note(self):
+        """Auto-save current note if modified"""
+        if (self.is_modified and 
+            self.note_title.text().strip() and 
+            settings.get("auto_save", True)):
+            
+            title = self.note_title.text()
+            content = self.note_text.toPlainText()
+            
+            # Use background thread for auto-save
+            self.autosave_thread.set_data(self.pin, title, content)
+            if not self.autosave_thread.isRunning():
+                self.autosave_thread.start()
+    
+    @pyqtSlot()
+    def on_autosave_complete(self):
+        """Handle auto-save completion"""
+        self.status_bar.showMessage("Auto-saved", 2000)

     def delete_note(self):
-        title = self.note_title.text()
-        if title:
-            delete_note(self.pin, title)
+        current_item = self.note_list.currentItem()
+        if not current_item:
+            QMessageBox.information(self, "Info", "Please select a note to delete")
+            return
+        
+        title = current_item.text()
+        
+        # Confirm deletion if enabled
+        if settings.get("confirm_delete", True):
+            reply = QMessageBox.question(
+                self, "Confirm Delete",
+                f"Are you sure you want to delete the note '{title}'?\n\n"
+                "This action cannot be undone.",
+                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
+                QMessageBox.StandardButton.No
+            )
+            
+            if reply != QMessageBox.StandardButton.Yes:
+                return
+        
+        try:
+            delete_note(self.pin, title)
             self.note_title.clear()
             self.note_text.clear()
+            self.current_note_title = None
+            self.is_modified = False
             self.refresh_notes()
+            self.update_ui_state()
+            
+            self.status_bar.showMessage(f"Note '{title}' deleted", 3000)
+            
+        except Exception as e:
+            QMessageBox.critical(self, "Error", f"Failed to delete note: {e}")

     def export_vault(self):
-        path, _ = QFileDialog.getSaveFileName(self, "Export Vault", "vault_backup.enc")
+        default_name = f"cryptex_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.enc"
+        path, _ = QFileDialog.getSaveFileName(
+            self, "Export Vault", default_name,
+            "Cryptex Vault (*.enc);;All Files (*)"
+        )
         if path:
-            export_vault(path)
-            QMessageBox.information(self, "Exported", "Vault exported successfully.")
+            try:
+                export_vault(path)
+                QMessageBox.information(self, "Export Successful", 
+                                      f"Vault exported to:\n{path}")
+                self.status_bar.showMessage("Vault exported successfully", 3000)
+            except Exception as e:
+                QMessageBox.critical(self, "Export Failed", f"Failed to export vault: {e}")

     def import_vault(self):
-        path, _ = QFileDialog.getOpenFileName(self, "Import Vault")
+        path, _ = QFileDialog.getOpenFileName(
+            self, "Import Vault", "",
+            "Cryptex Vault (*.enc);;All Files (*)"
+        )
         if path:
-            import_vault(path)
-            QMessageBox.information(self, "Imported", "Vault imported. Restart app to see changes.")
+            reply = QMessageBox.question(
+                self, "Confirm Import",
+                "Importing will replace your current vault.\n"
+                "Make sure you have a backup!\n\n"
+                "Continue with import?",
+                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
+            )
+            
+            if reply == QMessageBox.StandardButton.Yes:
+                try:
+                    import_vault(path)
+                    self.refresh_notes()
+                    QMessageBox.information(self, "Import Successful", 
+                                          "Vault imported successfully!")
+                    self.status_bar.showMessage("Vault imported successfully", 3000)
+                except Exception as e:
+                    QMessageBox.critical(self, "Import Failed", f"Failed to import vault: {e}")
+    
+    def focus_search(self):
+        """Focus search input"""
+        self.search_input.setFocus()
+        self.search_input.selectAll()
+    
+    def change_theme(self, theme_key):
+        """Change application theme"""
+        settings.set("theme", theme_key)
+        self.apply_theme()
+        
+        # Update status bar
+        theme_name = THEMES[theme_key]["name"]
+        self.theme_label.setText(f"Theme: {theme_name}")
+        self.status_bar.showMessage(f"Theme changed to {theme_name}", 3000)
+    
+    def open_settings(self):
+        """Open settings dialog"""
+        dialog = SettingsDialog(self.pin, self)
+        dialog.theme_changed.connect(self.on_theme_preview)
+        dialog.settings_changed.connect(self.on_settings_changed)
+        
+        if dialog.exec() == SettingsDialog.DialogCode.Accepted:
+            self.apply_theme()
+    
+    def on_theme_preview(self, theme_key):
+        """Preview theme change"""
+        self.setStyleSheet(generate_qss(theme_key))
+    
+    def on_settings_changed(self):
+        """Handle settings changes"""
+        # Update auto-save
+        if settings.get("auto_save", True):
+            interval = settings.get("auto_save_interval", 30) * 1000
+            self.autosave_timer.start(interval)
+            self.autosave_label.setText("Auto-save: ON")
+        else:
+            self.autosave_timer.stop()
+            self.autosave_label.setText("Auto-save: OFF")
+        
+        # Update note count display
+        self.refresh_notes()
+        
+        # Apply theme
+        self.apply_theme()
+        theme_name = THEMES[settings.get("theme", "dark_red")]["name"]
+        self.theme_label.setText(f"Theme: {theme_name}")
+    
+    def show_about(self):
+        """Show about dialog"""
+        QMessageBox.about(
+            self, "About Cryptex",
+            "<h2>Cryptex v2.0</h2>"
+            "<p><b>Enhanced Secure Note Manager</b></p>"
+            "<p>A modern, encrypted note-taking application with advanced features.</p>"
+            "<p><b>Features:</b></p>"
+            "<ul>"
+            "<li>🔒 Military-grade encryption</li>"
+            "<li>🎨 Multiple themes</li>"
+            "<li>💾 Auto-save functionality</li>"
+            "<li>🔍 Search and filter</li>"
+            "<li>📱 Modern, responsive UI</li>"
+            "<li>⚙️ Comprehensive settings</li>"
+            "</ul>"
+            "<p><b>Created by:</b> Mrtn777</p>"
+            "<p><b>Enhanced by:</b> Claude AI</p>"
+        )
+    
+    def closeEvent(self, event):
+        """Handle window close event"""
+        # Save current note if modified
+        if self.is_modified and self.current_note_title:
+            reply = QMessageBox.question(
+                self, "Unsaved Changes",
+                "You have unsaved changes. Save before closing?",
+                QMessageBox.StandardButton.Save | 
+                QMessageBox.StandardButton.Discard | 
+                QMessageBox.StandardButton.Cancel
+            )
+            
+            if reply == QMessageBox.StandardButton.Save:
+                self.save_note()
+            elif reply == QMessageBox.StandardButton.Cancel:
+                event.ignore()
+                return
+        
+        # Save window geometry
+        self.save_geometry()
+        
+        # Create backup if enabled
+        if settings.get("backup_on_exit", False):
+            try:
+                backup_path = f"data/auto_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.enc"
+                export_vault(backup_path)
+            except Exception:
+                pass  # Silent fail for auto-backup
+        
+        # Stop auto-save timer
+        self.autosave_timer.stop()
+        
+        event.accept()