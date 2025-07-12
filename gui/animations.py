"""Modern animation system for Cryptex"""
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QTimer, pyqtSignal, QObject, QRect, QPoint
from PyQt6.QtWidgets import QGraphicsOpacityEffect, QWidget, QGraphicsBlurEffect
from PyQt6.QtGui import QPainter, QColor, QPen

class ModernAnimator(QObject):
    """Modern animation manager with smooth effects"""
    
    def __init__(self):
        super().__init__()
        self.animations = []
    
    def fade_in(self, widget, duration=600):
        """Smooth fade in animation"""
        try:
            effect = QGraphicsOpacityEffect()
            widget.setGraphicsEffect(effect)
            
            animation = QPropertyAnimation(effect, b"opacity")
            animation.setDuration(duration)
            animation.setStartValue(0.0)
            animation.setEndValue(1.0)
            animation.setEasingCurve(QEasingCurve.Type.OutCubic)
            
            self.animations.append(animation)
            animation.start()
            return animation
        except Exception:
            widget.show()
            return None
    
    def scale_in(self, widget, duration=400):
        """Scale in animation for buttons"""
        try:
            original_size = widget.size()
            widget.resize(0, 0)
            
            animation = QPropertyAnimation(widget, b"size")
            animation.setDuration(duration)
            animation.setStartValue(widget.size())
            animation.setEndValue(original_size)
            animation.setEasingCurve(QEasingCurve.Type.OutBack)
            
            self.animations.append(animation)
            animation.start()
            return animation
        except Exception:
            return None
    
    def shake_error(self, widget, duration=500):
        """Shake animation for errors"""
        try:
            original_pos = widget.pos()
            
            animation = QPropertyAnimation(widget, b"pos")
            animation.setDuration(duration)
            animation.setEasingCurve(QEasingCurve.Type.InOutSine)
            
            # Create shake keyframes
            animation.setKeyValueAt(0.0, original_pos)
            animation.setKeyValueAt(0.1, QPoint(original_pos.x() - 10, original_pos.y()))
            animation.setKeyValueAt(0.2, QPoint(original_pos.x() + 10, original_pos.y()))
            animation.setKeyValueAt(0.3, QPoint(original_pos.x() - 8, original_pos.y()))
            animation.setKeyValueAt(0.4, QPoint(original_pos.x() + 8, original_pos.y()))
            animation.setKeyValueAt(0.5, QPoint(original_pos.x() - 5, original_pos.y()))
            animation.setKeyValueAt(0.6, QPoint(original_pos.x() + 5, original_pos.y()))
            animation.setKeyValueAt(0.7, QPoint(original_pos.x() - 2, original_pos.y()))
            animation.setKeyValueAt(0.8, QPoint(original_pos.x() + 2, original_pos.y()))
            animation.setKeyValueAt(1.0, original_pos)
            
            self.animations.append(animation)
            animation.start()
            return animation
        except Exception:
            return None
    
    def pulse_success(self, widget, duration=300):
        """Pulse animation for success"""
        try:
            original_style = widget.styleSheet()
            
            # Add glow effect
            widget.setStyleSheet(original_style + """
                border: 2px solid #10B981;
                box-shadow: 0 0 20px rgba(16, 185, 129, 0.5);
            """)
            
            def restore_style():
                widget.setStyleSheet(original_style)
            
            QTimer.singleShot(duration, restore_style)
        except Exception:
            pass
    
    def slide_up(self, widget, duration=500):
        """Slide up animation for cards"""
        try:
            original_pos = widget.pos()
            start_pos = QPoint(original_pos.x(), original_pos.y() + 50)
            widget.move(start_pos)
            
            animation = QPropertyAnimation(widget, b"pos")
            animation.setDuration(duration)
            animation.setStartValue(start_pos)
            animation.setEndValue(original_pos)
            animation.setEasingCurve(QEasingCurve.Type.OutCubic)
            
            self.animations.append(animation)
            animation.start()
            return animation
        except Exception:
            return None

# Global animator instance
animator = ModernAnimator()