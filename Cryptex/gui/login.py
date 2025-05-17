from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
import os
from core.auth import check_pin, set_pin
from gui.dashboard import Dashboard

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cryptex - Login")
        self.setStyleSheet(open("assets/dark.qss").read())
        self.setFixedSize(300, 200)
        layout = QVBoxLayout()

        self.label = QLabel("Enter PIN" if os.path.exists("data/pin.hash") else "Set a PIN")
        self.pin_input = QLineEdit()
        self.pin_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.button = QPushButton("Login" if os.path.exists("data/pin.hash") else "Set PIN")

        self.button.clicked.connect(self.handle_login)

        layout.addWidget(self.label)
        layout.addWidget(self.pin_input)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def handle_login(self):
        pin = self.pin_input.text()
        if os.path.exists("data/pin.hash"):
            if check_pin(pin):
                self.dashboard = Dashboard(pin)
                self.dashboard.show()
                self.close()
            else:
                QMessageBox.warning(self, "Error", "Incorrect PIN")
        else:
            set_pin(pin)
            QMessageBox.information(self, "PIN Set", "PIN has been set. Please restart the app.")
            self.close()