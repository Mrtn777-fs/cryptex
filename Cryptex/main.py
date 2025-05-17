from gui.login import LoginWindow
from PyQt6.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)
window = LoginWindow()
window.show()
sys.exit(app.exec())