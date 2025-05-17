from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QLineEdit, QListWidget, QMessageBox, QHBoxLayout
from core.database import load_data, save_data, delete_note, export_vault, import_vault
from PyQt6.QtWidgets import QFileDialog

class Dashboard(QWidget):
    def __init__(self, pin):
        super().__init__()
        self.pin = pin
        self.setWindowTitle("Cryptex")
        self.setFixedSize(600, 500)
        self.setStyleSheet(open("assets/dark.qss").read())

        layout = QVBoxLayout()

        self.note_list = QListWidget()
        self.note_list.itemClicked.connect(self.display_note)

        self.note_title = QLineEdit()
        self.note_title.setPlaceholderText("Title")

        self.note_text = QTextEdit()
        self.save_btn = QPushButton("Save Note")
        self.del_btn = QPushButton("Delete Note")
        self.exp_btn = QPushButton("Export Vault")
        self.imp_btn = QPushButton("Import Vault")

        self.save_btn.clicked.connect(self.save_note)
        self.del_btn.clicked.connect(self.delete_note)
        self.exp_btn.clicked.connect(self.export_vault)
        self.imp_btn.clicked.connect(self.import_vault)

        layout.addWidget(QLabel("Your Cryptex Notes"))
        layout.addWidget(self.note_list)
        layout.addWidget(self.note_title)
        layout.addWidget(self.note_text)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.del_btn)
        btn_layout.addWidget(self.exp_btn)
        btn_layout.addWidget(self.imp_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.refresh_notes()

    def refresh_notes(self):
        self.note_list.clear()
        self.notes = load_data(self.pin)
        for title in self.notes:
            self.note_list.addItem(title)

    def display_note(self, item):
        title = item.text()
        self.note_title.setText(title)
        self.note_text.setText(self.notes[title])

    def save_note(self):
        title = self.note_title.text()
        text = self.note_text.toPlainText()
        if title:
            save_data(self.pin, title, text)
            self.refresh_notes()

    def delete_note(self):
        title = self.note_title.text()
        if title:
            delete_note(self.pin, title)
            self.note_title.clear()
            self.note_text.clear()
            self.refresh_notes()

    def export_vault(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export Vault", "vault_backup.enc")
        if path:
            export_vault(path)
            QMessageBox.information(self, "Exported", "Vault exported successfully.")

    def import_vault(self):
        path, _ = QFileDialog.getOpenFileName(self, "Import Vault")
        if path:
            import_vault(path)
            QMessageBox.information(self, "Imported", "Vault imported. Restart app to see changes.")
