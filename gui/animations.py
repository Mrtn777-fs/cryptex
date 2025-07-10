"""Simple animation utilities for Cryptex GUI"""
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QTimer, pyqtSignal, QObject
from PyQt6.QtWidgets import QGraphicsOpacityEffect, QWidget

class AnimationManager(QObject):
    """Simple animation manager"""
    
    def __init__(self):
        super().__init__()
        self.animations = []
    
    def fade_in(self, widget, duration=300):
        """Simple fade in effect"""
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
        except:
            # If animation fails, just show the widget normally
            widget.show()
            return None
    
    def shake(self, widget, duration=500):
        """Simple shake effect for errors"""
        try:
            # Simple implementation - just flash the widget
            original_style = widget.styleSheet()
            widget.setStyleSheet(widget.styleSheet() + "; border: 2px solid red;")
            
            def restore_style():
                widget.setStyleSheet(original_style)
            
            QTimer.singleShot(duration, restore_style)
        except:
            # If animation fails, do nothing
            pass

# Global animation manager
animator = AnimationManager()