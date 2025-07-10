"""Theme definitions for Cryptex"""

THEMES = {
    "dark_red": {
        "name": "Dark Red (Classic)",
        "primary": "#cc2b2b",
        "primary_hover": "#ff4d4d",
        "primary_pressed": "#b71c1c",
        "background": "#1e1e1e",
        "surface": "#2a2a2a",
        "surface_hover": "#333333",
        "text": "#f2f2f2",
        "text_secondary": "#ff6666",
        "border": "#444444",
        "accent": "#e53935"
    },
    "dark_blue": {
        "name": "Dark Blue",
        "primary": "#1976d2",
        "primary_hover": "#42a5f5",
        "primary_pressed": "#0d47a1",
        "background": "#121212",
        "surface": "#1e1e1e",
        "surface_hover": "#2c2c2c",
        "text": "#ffffff",
        "text_secondary": "#64b5f6",
        "border": "#424242",
        "accent": "#2196f3"
    },
    "dark_purple": {
        "name": "Dark Purple",
        "primary": "#7b1fa2",
        "primary_hover": "#ab47bc",
        "primary_pressed": "#4a148c",
        "background": "#1a1a1a",
        "surface": "#2d2d2d",
        "surface_hover": "#3a3a3a",
        "text": "#f5f5f5",
        "text_secondary": "#ce93d8",
        "border": "#4a4a4a",
        "accent": "#9c27b0"
    },
    "dark_green": {
        "name": "Dark Green",
        "primary": "#388e3c",
        "primary_hover": "#66bb6a",
        "primary_pressed": "#1b5e20",
        "background": "#0d1b0d",
        "surface": "#1a2e1a",
        "surface_hover": "#2e4a2e",
        "text": "#e8f5e8",
        "text_secondary": "#81c784",
        "border": "#2e7d32",
        "accent": "#4caf50"
    },
    "cyberpunk": {
        "name": "Cyberpunk",
        "primary": "#ff0080",
        "primary_hover": "#ff33a1",
        "primary_pressed": "#cc0066",
        "background": "#0a0a0a",
        "surface": "#1a0a1a",
        "surface_hover": "#2a1a2a",
        "text": "#00ffff",
        "text_secondary": "#ff0080",
        "border": "#ff0080",
        "accent": "#00ff80"
    }
}

def generate_qss(theme_name):
    """Generate QSS stylesheet for the given theme"""
    theme = THEMES[theme_name]
    
    return f"""
    QWidget {{
        background-color: {theme['background']};
        color: {theme['text']};
        font-family: "Segoe UI", "SF Pro Display", Arial, sans-serif;
        font-size: 14px;
    }}

    QMainWindow {{
        background-color: {theme['background']};
    }}

    QLineEdit, QTextEdit {{
        background-color: {theme['surface']};
        color: {theme['text']};
        border: 2px solid {theme['primary']};
        border-radius: 8px;
        padding: 10px;
        selection-background-color: {theme['primary']};
        font-size: 14px;
    }}

    QLineEdit:focus, QTextEdit:focus {{
        border: 2px solid {theme['primary_hover']};
        background-color: {theme['surface_hover']};
    }}

    QLineEdit:hover, QTextEdit:hover {{
        background-color: {theme['surface_hover']};
    }}

    QPushButton {{
        background-color: {theme['primary']};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 20px;
        font-weight: 600;
        font-size: 14px;
        min-height: 20px;
    }}

    QPushButton:hover {{
        background-color: {theme['primary_hover']};
    }}

    QPushButton:pressed {{
        background-color: {theme['primary_pressed']};
    }}

    QPushButton:disabled {{
        background-color: #555555;
        color: #888888;
    }}

    QLabel {{
        font-weight: 600;
        color: {theme['text_secondary']};
        font-size: 14px;
    }}

    QLabel#title {{
        font-size: 24px;
        font-weight: 700;
        color: {theme['primary']};
        margin: 10px 0;
    }}

    QLabel#subtitle {{
        font-size: 16px;
        font-weight: 500;
        color: {theme['text_secondary']};
        margin: 5px 0;
    }}

    QListWidget {{
        background-color: {theme['surface']};
        border: 2px solid {theme['border']};
        border-radius: 8px;
        padding: 5px;
        outline: none;
    }}

    QListWidget::item {{
        background-color: transparent;
        color: {theme['text']};
        padding: 10px;
        border-radius: 6px;
        margin: 2px;
        border: 1px solid transparent;
    }}

    QListWidget::item:hover {{
        background-color: {theme['surface_hover']};
        border: 1px solid {theme['primary']};
    }}

    QListWidget::item:selected {{
        background-color: {theme['primary']};
        color: white;
        font-weight: 600;
    }}

    QScrollBar:vertical {{
        background: {theme['surface']};
        width: 12px;
        margin: 0;
        border: none;
        border-radius: 6px;
    }}

    QScrollBar::handle:vertical {{
        background: {theme['primary']};
        min-height: 20px;
        border-radius: 6px;
        margin: 2px;
    }}

    QScrollBar::handle:vertical:hover {{
        background: {theme['primary_hover']};
    }}

    QScrollBar::add-line:vertical,
    QScrollBar::sub-line:vertical {{
        height: 0px;
    }}

    QFrame {{
        background-color: {theme['surface']};
        border-radius: 12px;
        border: 1px solid {theme['border']};
        padding: 15px;
    }}

    QFrame#card {{
        background-color: {theme['surface']};
        border-radius: 12px;
        border: 2px solid {theme['border']};
        padding: 20px;
        margin: 10px;
    }}

    QComboBox {{
        background-color: {theme['surface']};
        color: {theme['text']};
        border: 2px solid {theme['primary']};
        border-radius: 8px;
        padding: 8px 12px;
        min-width: 150px;
    }}

    QComboBox:hover {{
        background-color: {theme['surface_hover']};
        border: 2px solid {theme['primary_hover']};
    }}

    QComboBox::drop-down {{
        border: none;
        width: 30px;
    }}

    QComboBox::down-arrow {{
        width: 0;
        height: 0;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 5px solid {theme['text']};
        margin-right: 10px;
    }}

    QComboBox QAbstractItemView {{
        background-color: {theme['surface']};
        color: {theme['text']};
        border: 2px solid {theme['primary']};
        border-radius: 8px;
        selection-background-color: {theme['primary']};
    }}

    QTabWidget::pane {{
        border: 2px solid {theme['border']};
        border-radius: 8px;
        background-color: {theme['surface']};
    }}

    QTabBar::tab {{
        background-color: {theme['surface']};
        color: {theme['text']};
        padding: 10px 20px;
        margin: 2px;
        border-radius: 6px;
        border: 1px solid {theme['border']};
    }}

    QTabBar::tab:selected {{
        background-color: {theme['primary']};
        color: white;
        font-weight: 600;
    }}

    QTabBar::tab:hover {{
        background-color: {theme['surface_hover']};
        border: 1px solid {theme['primary']};
    }}

    QCheckBox {{
        color: {theme['text']};
        font-size: 14px;
        spacing: 8px;
    }}

    QCheckBox::indicator {{
        width: 18px;
        height: 18px;
        border: 2px solid {theme['primary']};
        border-radius: 4px;
        background-color: {theme['surface']};
    }}

    QCheckBox::indicator:checked {{
        background-color: {theme['primary']};
    }}

    QSlider::groove:horizontal {{
        border: 1px solid {theme['border']};
        height: 6px;
        background: {theme['surface']};
        border-radius: 3px;
    }}

    QSlider::handle:horizontal {{
        background: {theme['primary']};
        border: 2px solid {theme['primary']};
        width: 18px;
        height: 18px;
        margin: -7px 0;
        border-radius: 9px;
    }}

    QSlider::handle:horizontal:hover {{
        background: {theme['primary_hover']};
        border: 2px solid {theme['primary_hover']};
    }}

    QProgressBar {{
        border: 2px solid {theme['border']};
        border-radius: 8px;
        text-align: center;
        background-color: {theme['surface']};
        color: {theme['text']};
        font-weight: 600;
    }}

    QProgressBar::chunk {{
        background-color: {theme['primary']};
        border-radius: 6px;
    }}

    QMessageBox {{
        background-color: {theme['background']};
        color: {theme['text']};
    }}

    QMessageBox QPushButton {{
        min-width: 80px;
        padding: 8px 16px;
    }}

    QToolTip {{
        background-color: {theme['surface']};
        color: {theme['text']};
        border: 1px solid {theme['primary']};
        border-radius: 6px;
        padding: 8px;
        font-size: 12px;
    }}

    QMenuBar {{
        background-color: {theme['surface']};
        color: {theme['text']};
        border-bottom: 1px solid {theme['border']};
    }}

    QMenuBar::item {{
        background-color: transparent;
        padding: 8px 12px;
    }}

    QMenuBar::item:selected {{
        background-color: {theme['primary']};
        color: white;
    }}

    QMenu {{
        background-color: {theme['surface']};
        color: {theme['text']};
        border: 1px solid {theme['border']};
        border-radius: 6px;
    }}

    QMenu::item {{
        padding: 8px 20px;
    }}

    QMenu::item:selected {{
        background-color: {theme['primary']};
        color: white;
    }}

    QToolBar {{
        background-color: {theme['surface']};
        border: none;
        spacing: 3px;
        padding: 5px;
    }}

    QToolBar QToolButton {{
        background-color: transparent;
        color: {theme['text']};
        border: none;
        padding: 8px 12px;
        border-radius: 6px;
    }}

    QToolBar QToolButton:hover {{
        background-color: {theme['surface_hover']};
    }}

    QToolBar QToolButton:pressed {{
        background-color: {theme['primary']};
        color: white;
    }}

    QStatusBar {{
        background-color: {theme['surface']};
        color: {theme['text']};
        border-top: 1px solid {theme['border']};
    }}
    """