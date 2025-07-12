"""Modern glassmorphism theme for Cryptex"""

# Color palette
COLORS = {
    "primary": "#00CFFF",           # Calm neon blue
    "secondary": "#8B5CF6",         # Soft purple
    "accent": "#14B8A6",            # Teal accent
    "background": "#0A0A0F",        # Deep dark background
    "surface": "#1A1A2E",           # Dark surface
    "glass": "rgba(26, 26, 46, 0.8)",  # Glass effect
    "text": "#FFFFFF",              # White text
    "text_secondary": "#A1A1AA",   # Gray text
    "success": "#10B981",           # Green
    "error": "#EF4444",             # Red
    "warning": "#F59E0B"            # Orange
}

def get_modern_qss():
    """Generate modern glassmorphism QSS"""
    return f"""
    /* Base styling */
    QWidget {{
        background-color: {COLORS['background']};
        color: {COLORS['text']};
        font-family: 'Inter', 'SF Pro Display', 'Segoe UI', sans-serif;
        font-size: 14px;
        font-weight: 400;
    }}

    /* Login window specific */
    QWidget#login-window {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #0A0A0F, stop:0.5 #1A1A2E, stop:1 #0A0A0F);
        border-radius: 24px;
    }}

    /* Glass panels */
    QFrame#glass-panel {{
        background: rgba(26, 26, 46, 0.8);
        border: 1px solid rgba(0, 207, 255, 0.3);
        border-radius: 16px;
        backdrop-filter: blur(20px);
    }}

    /* PIN input styling */
    QLineEdit#pin-input {{
        background: rgba(26, 26, 46, 0.6);
        border: 2px solid rgba(0, 207, 255, 0.4);
        border-radius: 16px;
        padding: 20px 24px;
        font-size: 24px;
        font-weight: 600;
        color: {COLORS['text']};
        letter-spacing: 8px;
        text-align: center;
    }}

    QLineEdit#pin-input:focus {{
        border: 2px solid {COLORS['primary']};
        background: rgba(26, 26, 46, 0.9);
        box-shadow: 0 0 20px rgba(0, 207, 255, 0.3);
    }}

    /* Primary buttons */
    QPushButton#primary {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 {COLORS['primary']}, stop:1 {COLORS['secondary']});
        color: white;
        border: none;
        border-radius: 16px;
        padding: 18px 32px;
        font-size: 16px;
        font-weight: 600;
        min-height: 20px;
    }}

    QPushButton#primary:hover {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 rgba(0, 207, 255, 0.9), stop:1 rgba(139, 92, 246, 0.9));
        transform: scale(1.02);
    }}

    QPushButton#primary:pressed {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 rgba(0, 207, 255, 0.7), stop:1 rgba(139, 92, 246, 0.7));
    }}

    /* Close button */
    QPushButton#close-btn {{
        background: rgba(239, 68, 68, 0.8);
        color: white;
        border: none;
        border-radius: 20px;
        font-size: 18px;
        font-weight: bold;
        min-width: 40px;
        min-height: 40px;
        max-width: 40px;
        max-height: 40px;
    }}

    QPushButton#close-btn:hover {{
        background: rgba(239, 68, 68, 1.0);
        transform: scale(1.1);
    }}

    /* Labels */
    QLabel#title {{
        font-size: 36px;
        font-weight: 700;
        color: {COLORS['primary']};
        margin: 20px 0;
    }}

    QLabel#subtitle {{
        font-size: 18px;
        font-weight: 500;
        color: {COLORS['text_secondary']};
        margin: 10px 0;
    }}

    QLabel#feature {{
        font-size: 14px;
        color: {COLORS['text_secondary']};
        padding: 8px 0;
    }}

    /* Checkbox */
    QCheckBox {{
        color: {COLORS['text_secondary']};
        font-size: 14px;
        font-weight: 500;
        spacing: 12px;
    }}

    QCheckBox::indicator {{
        width: 20px;
        height: 20px;
        border: 2px solid rgba(0, 207, 255, 0.5);
        border-radius: 6px;
        background: rgba(26, 26, 46, 0.6);
    }}

    QCheckBox::indicator:checked {{
        background: {COLORS['primary']};
        border: 2px solid {COLORS['primary']};
    }}

    /* Dashboard specific */
    QMainWindow {{
        background: {COLORS['background']};
    }}

    /* Sidebar */
    QFrame#sidebar {{
        background: rgba(26, 26, 46, 0.9);
        border: none;
        border-right: 1px solid rgba(0, 207, 255, 0.2);
    }}

    /* Note cards */
    QFrame#note-card {{
        background: rgba(26, 26, 46, 0.8);
        border: 1px solid rgba(0, 207, 255, 0.2);
        border-radius: 16px;
        padding: 20px;
        margin: 8px;
    }}

    QFrame#note-card:hover {{
        border: 1px solid rgba(0, 207, 255, 0.5);
        background: rgba(26, 26, 46, 0.9);
    }}

    /* List widgets */
    QListWidget {{
        background: rgba(26, 26, 46, 0.6);
        border: 1px solid rgba(0, 207, 255, 0.3);
        border-radius: 16px;
        padding: 12px;
        outline: none;
    }}

    QListWidget::item {{
        background: transparent;
        color: {COLORS['text']};
        padding: 16px 20px;
        border-radius: 12px;
        margin: 4px 0;
        border: 1px solid transparent;
        font-weight: 500;
    }}

    QListWidget::item:hover {{
        background: rgba(0, 207, 255, 0.1);
        border: 1px solid rgba(0, 207, 255, 0.3);
    }}

    QListWidget::item:selected {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 rgba(0, 207, 255, 0.3), stop:1 rgba(139, 92, 246, 0.3));
        border: 1px solid {COLORS['primary']};
        color: white;
        font-weight: 600;
    }}

    /* Text areas */
    QTextEdit {{
        background: rgba(26, 26, 46, 0.6);
        border: 2px solid rgba(0, 207, 255, 0.3);
        border-radius: 16px;
        padding: 20px;
        font-size: 16px;
        line-height: 1.6;
        color: {COLORS['text']};
    }}

    QTextEdit:focus {{
        border: 2px solid {COLORS['primary']};
        background: rgba(26, 26, 46, 0.8);
    }}

    /* Scrollbars */
    QScrollBar:vertical {{
        background: rgba(26, 26, 46, 0.5);
        width: 12px;
        border-radius: 6px;
        margin: 0;
    }}

    QScrollBar::handle:vertical {{
        background: {COLORS['primary']};
        border-radius: 6px;
        min-height: 20px;
        margin: 2px;
    }}

    QScrollBar::handle:vertical:hover {{
        background: rgba(0, 207, 255, 0.8);
    }}

    QScrollBar::add-line:vertical,
    QScrollBar::sub-line:vertical {{
        height: 0px;
    }}

    /* Menu styling */
    QMenuBar {{
        background: rgba(26, 26, 46, 0.9);
        color: {COLORS['text']};
        border: none;
        padding: 8px;
        font-weight: 500;
    }}

    QMenuBar::item {{
        background: transparent;
        padding: 12px 16px;
        border-radius: 8px;
    }}

    QMenuBar::item:selected {{
        background: rgba(0, 207, 255, 0.2);
        color: {COLORS['primary']};
    }}

    QMenu {{
        background: rgba(26, 26, 46, 0.95);
        border: 1px solid rgba(0, 207, 255, 0.3);
        border-radius: 12px;
        padding: 8px;
    }}

    QMenu::item {{
        padding: 12px 20px;
        border-radius: 8px;
        font-weight: 500;
    }}

    QMenu::item:selected {{
        background: rgba(0, 207, 255, 0.2);
        color: {COLORS['primary']};
    }}

    /* Status bar */
    QStatusBar {{
        background: rgba(26, 26, 46, 0.9);
        color: {COLORS['text_secondary']};
        border: none;
        border-top: 1px solid rgba(0, 207, 255, 0.2);
        font-size: 12px;
        padding: 8px;
    }}
    """