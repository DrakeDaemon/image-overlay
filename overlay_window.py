from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import Qt, QPoint
import os

class OverlayWindow(QWidget):
    def __init__(self, image_path, scale_factor=1.0, movable=False, 
                 position_x=100, position_y=100, position_callback=None):
        super().__init__()
        self.image_path = image_path
        self.scale_factor = scale_factor
        self.movable = movable
        self.position_x = position_x
        self.position_y = position_y
        self.position_callback = position_callback
        self.pixmap = None
        self.drag_position = QPoint()
        
        self.init_ui()
        self.load_image()
    
    def init_ui(self):
        """Initialize the UI"""
        # Set window properties
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        
        # Set transparency
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Position window
        self.move(self.position_x, self.position_y)
    
    def load_image(self):
        """Load and display the overlay image"""
        try:
            if not os.path.exists(self.image_path):
                print(f"Image not found: {self.image_path}")
                # Use a default image if the specified one doesn't exist
                self.image_path = "assets/default_overlay.png"
                if not os.path.exists(self.image_path):
                    return
            
            # Load image
            self.pixmap = QPixmap(self.image_path)
            
            # Apply scaling
            if self.scale_factor != 1.0:
                new_width = int(self.pixmap.width() * self.scale_factor)
                new_height = int(self.pixmap.height() * self.scale_factor)
                self.pixmap = self.pixmap.scaled(
                    new_width, 
                    new_height,
                    Qt.AspectRatioMode.IgnoreAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
            
            # Resize window to fit the image
            self.resize(self.pixmap.width(), self.pixmap.height())
            
        except Exception as e:
            print(f"Error loading image: {e}")
    
    def paintEvent(self, event):
        """Paint the image on the window"""
        if self.pixmap:
            painter = QPainter(self)
            painter.drawPixmap(0, 0, self.pixmap)
    
    def mousePressEvent(self, event):
        """Handle mouse press for dragging"""
        if self.movable and event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
        else:
            super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        """Handle mouse movement for dragging"""
        if self.movable and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
        else:
            super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release after dragging"""
        if self.movable and event.button() == Qt.MouseButton.LeftButton:
            # Save the new position
            if self.position_callback:
                self.position_callback(self.x(), self.y())
            event.accept()
        else:
            super().mouseReleaseEvent(event)
    
    def update_scale(self, scale_factor):
        """Update the overlay scale"""
        if scale_factor != self.scale_factor:
            self.scale_factor = scale_factor
            self.load_image()  # Reload image with new scale
            self.update()
    
    def update_movable(self, movable):
        """Update the overlay movable property"""
        if movable != self.movable:
            self.movable = movable
            
            # Update window flags based on movability
            if self.movable:
                self.setWindowFlags(
                    Qt.WindowType.FramelessWindowHint |
                    Qt.WindowType.WindowStaysOnTopHint
                )
            else:
                self.setWindowFlags(
                    Qt.WindowType.FramelessWindowHint |
                    Qt.WindowType.WindowStaysOnTopHint |
                    Qt.WindowType.Tool
                )
            
            # Re-show the window to apply changes
            self.show()
    
    def update_image(self, image_path):
        """Update the overlay image"""
        self.image_path = image_path
        self.load_image()
        self.update()