"""Modern theme definitions for Cryptex"""

THEMES = {
    "dark_modern": {
        "name": "Dark Modern",
        "primary": "#6366f1",
        "primary_hover": "#7c3aed",
        "primary_pressed": "#4f46e5",
        "background": "#0f0f23",
        "surface": "#1a1a2e",
        "surface_hover": "#16213e",
        "text": "#ffffff",
        "text_secondary": "#a1a1aa",
        "border": "#374151",
        "accent": "#8b5cf6",
        "success": "#10b981",
        "error": "#ef4444",
        "warning": "#f59e0b"
    },
    "cyberpunk": {
        "name": "Cyberpunk",
        "primary": "#ff0080",
        "primary_hover": "#ff1a8c",
        "primary_pressed": "#e6006b",
        "background": "#0a0a0a",
        "surface": "#1a0a1a",
        "surface_hover": "#2a1a2a",
        "text": "#00ffff",
        "text_secondary": "#ff0080",
        "border": "#ff0080",
        "accent": "#00ff80",
        "success": "#00ff80",
        "error": "#ff0040",
        "warning": "#ffff00"
    },
    "ocean": {
        "name": "Ocean Blue",
        "primary": "#0ea5e9",
        "primary_hover": "#0284c7",
        "primary_pressed": "#0369a1",
        "background": "#0c1222",
        "surface": "#1e293b",
        "surface_hover": "#334155",
        "text": "#f8fafc",
        "text_secondary": "#94a3b8",
        "border": "#475569",
        "accent": "#06b6d4",
        "success": "#22c55e",
        "error": "#ef4444",
        "warning": "#f59e0b"
    },
    "forest": {
        "name": "Forest Green",
        "primary": "#22c55e",
        "primary_hover": "#16a34a",
        "primary_pressed": "#15803d",
        "background": "#0f1419",
        "surface": "#1a2e1a",
        "surface_hover": "#2d4a2d",
        "text": "#f0fdf4",
        "text_secondary": "#86efac",
        "border": "#166534",
        "accent": "#4ade80",
        "success": "#22c55e",
        "error": "#ef4444",
        "warning": "#f59e0b"
    },
    "sunset": {
        "name": "Sunset Orange",
        "primary": "#f97316",
        "primary_hover": "#ea580c",
        "primary_pressed": "#c2410c",
        "background": "#1c1917",
        "surface": "#292524",
        "surface_hover": "#44403c",
        "text": "#fafaf9",
        "text_secondary": "#fdba74",
        "border": "#78716c",
        "accent": "#fb923c",
        "success": "#22c55e",
        "error": "#ef4444",
        "warning": "#f59e0b"
    }
}

def generate_qss(theme_name):
    """Generate clean QSS stylesheet for the given theme"""
    theme = THEMES[theme_name]
    
    return f"""
    /* Base Widget Styling */
    QWidget {{
        background-color: {theme['background']};
        color: {theme['text']};
        font-family: "Segoe UI", "SF Pro Display", "Inter", sans-serif;
        font-size: 14px;
        font-weight: 400;
    }}

    QMainWindow {{
        background-color: {theme['background']};
    }}

    /* Input Fields */
    QLineEdit, QTextEdit {{
        background-color: {theme['surface']};
        color: {theme['text']};
        border: 2px solid {theme['border']};
        border-radius: 12px;
        padding: 16px 20px;
        font-size: 15px;
        font-weight: 500;
        selection-background-color: {theme['primary']};
    }}

    QLineEdit:focus, QTextEdit:focus {{
        border: 2px solid {theme['primary']};
        background-color: {theme['surface_hover']};
    }}

    QLineEdit:hover, QTextEdit:hover {{
        background-color: {theme['surface_hover']};
        border: 2px solid {theme['primary_hover']};
    }}

    /* Buttons */
    QPushButton {{
        background-color: {theme['primary']};
        color: white;
        border: none;
        border-radius: 12px;
        padding: 16px 24px;
        font-weight: 600;
        font-size: 15px;
        min-height: 20px;
    }}

    QPushButton:hover {{
        background-color: {theme['primary_hover']};
    }}

    QPushButton:pressed {{
        background-color: {theme['primary_pressed']};
    }}

    QPushButton:disabled {{
        background-color: {theme['border']};
        color: {theme['text_secondary']};
    }}

    QPushButton#secondary {{
        background-color: {theme['surface']};
        color: {theme['text']};
        border: 2px solid {theme['border']};
    }}

    QPushButton#secondary:hover {{
        background-color: {theme['surface_hover']};
        border: 2px solid {theme['primary']};
    }}

    QPushButton#danger {{
        background-color: {theme['error']};
    }}

    QPushButton#danger:hover {{
        background-color: #dc2626;
    }}

    /* Labels */
    QLabel {{
        color: {theme['text']};
        font-weight: 500;
    }}

    QLabel#title {{
        font-size: 32px;
        font-weight: 700;
        color: {theme['primary']};
        margin: 20px 0;
    }}

    QLabel#subtitle {{
        font-size: 18px;
        font-weight: 500;
        color: {theme['text_secondary']};
        margin: 10px 0;
    }}

    QLabel#heading {{
        font-size: 20px;
        font-weight: 600;
        color: {theme['text']};
        margin: 15px 0 10px 0;
    }}

    QLabel#caption {{
        font-size: 13px;
        color: {theme['text_secondary']};
        font-weight: 400;
    }}

    /* Cards and Frames */
    QFrame {{
        background-color: {theme['surface']};
        border-radius: 16px;
        border: 1px solid {theme['border']};
        padding: 20px;
    }}

    QFrame#card {{
        background-color: {theme['surface']};
        border-radius: 20px;
        border: 1px solid {theme['border']};
        padding: 30px;
        margin: 10px;
    }}

    QFrame#login-card {{
        background-color: {theme['surface']};
        border-radius: 24px;
        border: 1px solid {theme['border']};
        padding: 40px;
        margin: 20px;
    }}

    /* List Widgets */
    QListWidget {{
        background-color: {theme['surface']};
        border: 1px solid {theme['border']};
        border-radius: 12px;
        padding: 8px;
        outline: none;
    }}

    QListWidget::item {{
        background-color: transparent;
        color: {theme['text']};
        padding: 12px 16px;
        border-radius: 8px;
        margin: 2px 0;
        border: none;
    }}

    QListWidget::item:hover {{
        background-color: {theme['surface_hover']};
    }}

    QListWidget::item:selected {{
        background-color: {theme['primary']};
        color: white;
        font-weight: 600;
    }}

    /* Scrollbars */
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

    /* Combo Boxes */
    QComboBox {{
        background-color: {theme['surface']};
        color: {theme['text']};
        border: 2px solid {theme['border']};
        border-radius: 12px;
        padding: 12px 16px;
        min-width: 150px;
        font-weight: 500;
    }}

    QComboBox:hover {{
        background-color: {theme['surface_hover']};
        border: 2px solid {theme['primary']};
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
        border: 2px solid {theme['border']};
        border-radius: 12px;
        selection-background-color: {theme['primary']};
        padding: 4px;
    }}

    /* Checkboxes */
    QCheckBox {{
        color: {theme['text']};
        font-size: 14px;
        font-weight: 500;
        spacing: 12px;
    }}

    QCheckBox::indicator {{
        width: 20px;
        height: 20px;
        border: 2px solid {theme['border']};
        border-radius: 6px;
        background-color: {theme['surface']};
    }}

    QCheckBox::indicator:checked {{
        background-color: {theme['primary']};
        border: 2px solid {theme['primary']};
    }}

    QCheckBox::indicator:hover {{
        border: 2px solid {theme['primary']};
    }}

    /* Progress Bars */
    QProgressBar {{
        border: none;
        border-radius: 8px;
        text-align: center;
        background-color: {theme['surface']};
        color: {theme['text']};
        font-weight: 600;
        height: 8px;
    }}

    QProgressBar::chunk {{
        background-color: {theme['primary']};
        border-radius: 8px;
    }}

    /* Menu Bar */
    QMenuBar {{
        background-color: {theme['surface']};
        color: {theme['text']};
        border-bottom: 1px solid {theme['border']};
        padding: 4px;
    }}

    QMenuBar::item {{
        background-color: transparent;
        padding: 8px 16px;
        border-radius: 8px;
        font-weight: 500;
    }}

    QMenuBar::item:selected {{
        background-color: {theme['primary']};
        color: white;
    }}

    QMenu {{
        background-color: {theme['surface']};
        color: {theme['text']};
        border: 1px solid {theme['border']};
        border-radius: 12px;
        padding: 8px;
    }}

    QMenu::item {{
        padding: 10px 20px;
        border-radius: 8px;
        font-weight: 500;
    }}

    QMenu::item:selected {{
        background-color: {theme['primary']};
        color: white;
    }}

    /* Toolbar */
    QToolBar {{
        background-color: {theme['surface']};
        border: none;
        spacing: 8px;
        padding: 8px;
    }}

    QToolBar QToolButton {{
        background-color: transparent;
        color: {theme['text']};
        border: none;
        padding: 10px 16px;
        border-radius: 8px;
        font-weight: 500;
    }}

    QToolBar QToolButton:hover {{
        background-color: {theme['surface_hover']};
    }}

    QToolBar QToolButton:pressed {{
        background-color: {theme['primary']};
        color: white;
    }}

    /* Status Bar */
    QStatusBar {{
        background-color: {theme['surface']};
        color: {theme['text_secondary']};
        border-top: 1px solid {theme['border']};
        font-size: 12px;
        padding: 4px;
    }}

    /* Tabs */
    QTabWidget::pane {{
        border: 1px solid {theme['border']};
        border-radius: 12px;
        background-color: {theme['surface']};
        top: -1px;
    }}

    QTabBar::tab {{
        background-color: {theme['surface']};
        color: {theme['text_secondary']};
        padding: 12px 20px;
        margin: 2px;
        border-radius: 8px;
        font-weight: 500;
    }}

    QTabBar::tab:selected {{
        background-color: {theme['primary']};
        color: white;
        font-weight: 600;
    }}

    QTabBar::tab:hover {{
        background-color: {theme['surface_hover']};
        color: {theme['text']};
    }}

    /* Splitter */
    QSplitter::handle {{
        background-color: {theme['border']};
        width: 2px;
        height: 2px;
    }}

    QSplitter::handle:hover {{
        background-color: {theme['primary']};
    }}

    /* Message Boxes */
    QMessageBox {{
        background-color: {theme['background']};
        color: {theme['text']};
    }}

    QMessageBox QPushButton {{
        min-width: 80px;
        padding: 10px 20px;
    }}

    /* Tooltips */
    QToolTip {{
        background-color: {theme['surface']};
        color: {theme['text']};
        border: 1px solid {theme['border']};
        border-radius: 8px;
        padding: 8px 12px;
        font-size: 12px;
        font-weight: 500;
    }}
    """