"""
Smooth animations for Cryptex using PyQt6
"""
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QTimer, pyqtSignal, QObject
from PyQt6.QtWidgets import QGraphicsOpacityEffect
from PyQt6.QtGui import QFont

class AnimationManager(QObject):
    """Manages all animations in the application"""
    
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
    
    def fade_out(self, widget, duration=300):
        """Fade out animation"""
        effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(effect)
        
        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(1.0)
        animation.setEndValue(0.0)
        animation.setEasingCurve(QEasingCurve.Type.InCubic)
        
        self.animations.append(animation)
        animation.start()
        return animation
    
    def shake_widget(self, widget, duration=500):
        """Shake animation for errors"""
        animation = QPropertyAnimation(widget, b"pos")
        animation.setDuration(duration)
        animation.setEasingCurve(QEasingCurve.Type.OutBounce)
        
        start_pos = widget.pos()
        animation.setStartValue(start_pos)
        animation.setKeyValueAt(0.1, start_pos + widget.rect().topLeft() + widget.rect().center() * 0.02)
        animation.setKeyValueAt(0.2, start_pos - widget.rect().topLeft() - widget.rect().center() * 0.02)
        animation.setKeyValueAt(0.3, start_pos + widget.rect().topLeft() + widget.rect().center() * 0.01)
        animation.setKeyValueAt(0.4, start_pos - widget.rect().topLeft() - widget.rect().center() * 0.01)
        animation.setEndValue(start_pos)
        
        self.animations.append(animation)
        animation.start()
        return animation
    
    def pulse_widget(self, widget, duration=200):
        """Pulse animation for success"""
        original_font = widget.font()
        larger_font = QFont(original_font)
        larger_font.setPointSize(original_font.pointSize() + 2)
        
        # Pulse effect using font size
        def pulse_step1():
            widget.setFont(larger_font)
            QTimer.singleShot(duration // 2, pulse_step2)
        
        def pulse_step2():
            widget.setFont(original_font)
        
        pulse_step1()
    
    def smooth_transition(self, widget, property_name, start_value, end_value, duration=300):
        """Generic smooth transition animation"""
        animation = QPropertyAnimation(widget, property_name.encode())
        animation.setDuration(duration)
        animation.setStartValue(start_value)
        animation.setEndValue(end_value)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        self.animations.append(animation)
        animation.start()
        return animation

# Global animation manager
animator = AnimationManager()