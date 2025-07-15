"""
Modern theme system for Cryptex with multiple beautiful themes
"""

THEMES = {
    "cyber_blue": {
        "name": "Cyber Blue",
        "primary": "#00CFFF",
        "secondary": "#0099CC",
        "accent": "#66D9FF",
        "background": "#0a0a0a",
        "surface": "#1a1a1a",
        "card": "#2a2a2a",
        "text": "#ffffff",
        "text_secondary": "#cccccc",
        "success": "#00ff88",
        "error": "#ff4444",
        "warning": "#ffaa00"
    },
    "neon_purple": {
        "name": "Neon Purple",
        "primary": "#8B5CF6",
        "secondary": "#7C3AED",
        "accent": "#A78BFA",
        "background": "#0f0a1a",
        "surface": "#1a0f2e",
        "card": "#2a1f3d",
        "text": "#ffffff",
        "text_secondary": "#d1c7e8",
        "success": "#10b981",
        "error": "#ef4444",
        "warning": "#f59e0b"
    },
    "emerald_dark": {
        "name": "Emerald Dark",
        "primary": "#10b981",
        "secondary": "#059669",
        "accent": "#34d399",
        "background": "#0a1a0f",
        "surface": "#0f2a1a",
        "card": "#1a3d2a",
        "text": "#ffffff",
        "text_secondary": "#c7e8d1",
        "success": "#22c55e",
        "error": "#ef4444",
        "warning": "#f59e0b"
    },
    "sunset_orange": {
        "name": "Sunset Orange",
        "primary": "#f97316",
        "secondary": "#ea580c",
        "accent": "#fb923c",
        "background": "#1a0f0a",
        "surface": "#2a1a0f",
        "card": "#3d2a1a",
        "text": "#ffffff",
        "text_secondary": "#e8d7c7",
        "success": "#22c55e",
        "error": "#ef4444",
        "warning": "#eab308"
    }
}

def generate_qss(theme_name="cyber_blue"):
    """Generate QSS stylesheet for the given theme"""
    theme = THEMES.get(theme_name, THEMES["cyber_blue"])
    
    return f"""
    /* Main Application Styling */
    QWidget {{
        background-color: {theme['background']};
        color: {theme['text']};
        font-family: 'Segoe UI', 'SF Pro Display', 'Inter', sans-serif;
        font-size: 14px;
    }}
    
    /* Login Window Specific */
    QWidget#LoginWindow {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 {theme['background']}, 
            stop:0.5 {theme['surface']}, 
            stop:1 {theme['background']});
    }}
    
    /* Main Card Styling */
    QFrame#MainCard {{
        background-color: {theme['card']};
        border: 2px solid {theme['primary']};
        border-radius: 20px;
        padding: 30px;
    }}
    
    /* Title Labels */
    QLabel#Title {{
        color: {theme['primary']};
        font-size: 36px;
        font-weight: bold;
        margin-bottom: 10px;
    }}
    
    QLabel#Subtitle {{
        color: {theme['text_secondary']};
        font-size: 16px;
        margin-bottom: 30px;
    }}
    
    /* PIN Input Field */
    QLineEdit#PinInput {{
        background-color: {theme['surface']};
        border: 3px solid {theme['primary']};
        border-radius: 15px;
        padding: 20px;
        font-size: 24px;
        font-weight: bold;
        color: {theme['text']};
        text-align: center;
        letter-spacing: 8px;
    }}
    
    QLineEdit#PinInput:focus {{
        border-color: {theme['accent']};
        background-color: {theme['card']};
    }}
    
    /* Primary Buttons */
    QPushButton#PrimaryButton {{
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 {theme['primary']}, 
            stop:1 {theme['secondary']});
        color: {theme['background']};
        border: none;
        border-radius: 12px;
        padding: 15px 30px;
        font-size: 16px;
        font-weight: bold;
    }}
    
    QPushButton#PrimaryButton:hover {{
        background: {theme['accent']};
    }}
    
    QPushButton#PrimaryButton:pressed {{
        background: {theme['secondary']};
    }}
    
    /* Secondary Buttons */
    QPushButton#SecondaryButton {{
        background-color: transparent;
        color: {theme['primary']};
        border: 2px solid {theme['primary']};
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 14px;
        font-weight: bold;
    }}
    
    QPushButton#SecondaryButton:hover {{
        background-color: {theme['primary']};
        color: {theme['background']};
    }}
    
    /* Dashboard Styling */
    QFrame#Sidebar {{
        background-color: {theme['surface']};
        border-right: 2px solid {theme['primary']};
        padding: 20px;
    }}
    
    QFrame#MainPanel {{
        background-color: {theme['background']};
        padding: 20px;
    }}
    
    /* Note Cards */
    QFrame#NoteCard {{
        background-color: {theme['card']};
        border: 1px solid {theme['primary']};
        border-radius: 12px;
        padding: 15px;
        margin: 5px;
    }}
    
    QFrame#NoteCard:hover {{
        border-color: {theme['accent']};
        background-color: {theme['surface']};
    }}
    
    /* Input Fields */
    QLineEdit, QTextEdit {{
        background-color: {theme['surface']};
        border: 2px solid {theme['primary']};
        border-radius: 8px;
        padding: 12px;
        color: {theme['text']};
        font-size: 14px;
    }}
    
    QLineEdit:focus, QTextEdit:focus {{
        border-color: {theme['accent']};
        background-color: {theme['card']};
    }}
    
    /* List Widgets */
    QListWidget {{
        background-color: {theme['surface']};
        border: 2px solid {theme['primary']};
        border-radius: 8px;
        padding: 5px;
    }}
    
    QListWidget::item {{
        background-color: {theme['card']};
        border: 1px solid {theme['primary']};
        border-radius: 6px;
        padding: 12px;
        margin: 3px;
        color: {theme['text']};
    }}
    
    QListWidget::item:selected {{
        background-color: {theme['primary']};
        color: {theme['background']};
    }}
    
    QListWidget::item:hover {{
        background-color: {theme['accent']};
        color: {theme['background']};
    }}
    
    /* Menu Bar */
    QMenuBar {{
        background-color: {theme['surface']};
        color: {theme['text']};
        border-bottom: 2px solid {theme['primary']};
        padding: 5px;
    }}
    
    QMenuBar::item {{
        background-color: transparent;
        padding: 8px 15px;
        border-radius: 6px;
    }}
    
    QMenuBar::item:selected {{
        background-color: {theme['primary']};
        color: {theme['background']};
    }}
    
    QMenu {{
        background-color: {theme['card']};
        border: 2px solid {theme['primary']};
        border-radius: 8px;
        padding: 5px;
    }}
    
    QMenu::item {{
        padding: 8px 20px;
        border-radius: 4px;
    }}
    
    QMenu::item:selected {{
        background-color: {theme['primary']};
        color: {theme['background']};
    }}
    
    /* Combo Box */
    QComboBox {{
        background-color: {theme['surface']};
        border: 2px solid {theme['primary']};
        border-radius: 8px;
        padding: 8px 12px;
        color: {theme['text']};
    }}
    
    QComboBox:hover {{
        border-color: {theme['accent']};
    }}
    
    QComboBox::drop-down {{
        border: none;
        width: 20px;
    }}
    
    QComboBox::down-arrow {{
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 5px solid {theme['primary']};
        margin-right: 5px;
    }}
    
    QComboBox QAbstractItemView {{
        background-color: {theme['card']};
        border: 2px solid {theme['primary']};
        border-radius: 8px;
        selection-background-color: {theme['primary']};
        selection-color: {theme['background']};
    }}
    
    /* Status Bar */
    QStatusBar {{
        background-color: {theme['surface']};
        color: {theme['text_secondary']};
        border-top: 1px solid {theme['primary']};
    }}
    
    /* Error Styling */
    QLineEdit#ErrorInput {{
        border-color: {theme['error']} !important;
        background-color: {theme['surface']} !important;
    }}
    
    /* Success Styling */
    QLabel#SuccessLabel {{
        color: {theme['success']};
        font-weight: bold;
    }}
    
    /* Info Labels */
    QLabel#InfoLabel {{
        color: {theme['text_secondary']};
        font-size: 12px;
    }}
    """