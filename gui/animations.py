"""Animation utilities for Cryptex GUI"""
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QRect, QTimer, pyqtSignal, QObject
from PyQt6.QtWidgets import QGraphicsOpacityEffect, QWidget
from PyQt6.QtGui import QColor

class AnimationManager(QObject):
    """Manages animations for widgets"""
    
    def __init__(self):
        super().__init__()
        self.animations = []
    
    def fade_in(self, widget, duration=300):
        """Fade in animation"""
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
    
    def fade_out(self, widget, duration=300, callback=None):
        """Fade out animation"""
        effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(effect)
        
        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(1.0)
        animation.setEndValue(0.0)
        animation.setEasingCurve(QEasingCurve.Type.InCubic)
        
        if callback:
            animation.finished.connect(callback)
        
        self.animations.append(animation)
        animation.start()
        return animation
    
    def slide_in_from_right(self, widget, duration=400):
        """Slide in from right animation"""
        start_pos = widget.pos()
        widget.move(start_pos.x() + widget.width(), start_pos.y())
        
        animation = QPropertyAnimation(widget, b"pos")
        animation.setDuration(duration)
        animation.setEndValue(start_pos)
        animation.setEasingCurve(QEasingCurve.Type.OutBack)
        
        self.animations.append(animation)
        animation.start()
        return animation
    
    def bounce_in(self, widget, duration=600):
        """Bounce in animation"""
        original_size = widget.size()
        widget.resize(0, 0)
        
        animation = QPropertyAnimation(widget, b"size")
        animation.setDuration(duration)
        animation.setEndValue(original_size)
        animation.setEasingCurve(QEasingCurve.Type.OutBounce)
        
        self.animations.append(animation)
        animation.start()
        return animation
    
    def shake(self, widget, duration=500):
        """Shake animation for errors"""
        original_pos = widget.pos()
        
        animation = QPropertyAnimation(widget, b"pos")
        animation.setDuration(duration)
        animation.setKeyValueAt(0.0, original_pos)
        animation.setKeyValueAt(0.1, original_pos + QRect(10, 0, 0, 0).topLeft())
        animation.setKeyValueAt(0.2, original_pos + QRect(-10, 0, 0, 0).topLeft())
        animation.setKeyValueAt(0.3, original_pos + QRect(8, 0, 0, 0).topLeft())
        animation.setKeyValueAt(0.4, original_pos + QRect(-8, 0, 0, 0).topLeft())
        animation.setKeyValueAt(0.5, original_pos + QRect(5, 0, 0, 0).topLeft())
        animation.setKeyValueAt(0.6, original_pos + QRect(-5, 0, 0, 0).topLeft())
        animation.setKeyValueAt(0.7, original_pos + QRect(2, 0, 0, 0).topLeft())
        animation.setKeyValueAt(0.8, original_pos + QRect(-2, 0, 0, 0).topLeft())
        animation.setKeyValueAt(1.0, original_pos)
        
        self.animations.append(animation)
        animation.start()
        return animation
    
    def pulse(self, widget, duration=1000):
        """Pulse animation"""
        effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(effect)
        
        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(1.0)
        animation.setKeyValueAt(0.5, 0.5)
        animation.setEndValue(1.0)
        animation.setLoopCount(-1)  # Infinite loop
        animation.setEasingCurve(QEasingCurve.Type.InOutSine)
        
        self.animations.append(animation)
        animation.start()
        return animation

# Global animation manager
animator = AnimationManager()