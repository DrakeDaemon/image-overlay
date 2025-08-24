from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QCheckBox, QPushButton, QGroupBox, 
                             QRadioButton, QFileDialog, QLineEdit, QButtonGroup,
                             QApplication)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QScreen
import os

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("Image Overlay Settings")
        self.setFixedSize(500, 200)  # Fixed size for better centering
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Enable overlay checkbox
        self.enable_checkbox = QCheckBox("Enable Overlay")
        layout.addWidget(self.enable_checkbox)
        
        # Image selection
        image_layout = QHBoxLayout()
        image_layout.addWidget(QLabel("Overlay Image:"))
        
        self.image_path_edit = QLineEdit()
        image_layout.addWidget(self.image_path_edit)
        
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_image)
        image_layout.addWidget(self.browse_button)
        
        layout.addLayout(image_layout)
        
        # Scale factor selection
        scale_group = QGroupBox("Image Scaling")
        scale_layout = QHBoxLayout()
        
        self.scale_group = QButtonGroup(self)
        scales = [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0]
        
        for scale in scales:
            radio = QRadioButton(f"{scale}x")
            radio.setProperty("scale_value", scale)
            self.scale_group.addButton(radio)
            scale_layout.addWidget(radio)
            if scale == 1.0:
                radio.setChecked(True)
        
        scale_group.setLayout(scale_layout)
        layout.addWidget(scale_group)
        
        # Movable overlay option
        self.movable_checkbox = QCheckBox("Movable Overlay (drag to position)")
        layout.addWidget(self.movable_checkbox)
        
        # Load current settings
        self.load_settings()
        
        # Connect signals after loading settings to avoid triggering events during initialization
        self.enable_checkbox.stateChanged.connect(self.toggle_overlay)
        self.scale_group.buttonClicked.connect(self.update_scale)
        self.movable_checkbox.stateChanged.connect(self.update_movable)
        
        # Add stretch to push everything to the top
        layout.addStretch()
    
    def center(self):
        """Center the window on the screen"""
        # Get the screen geometry
        screen = QApplication.primaryScreen().geometry()
        
        # Calculate the center position
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        
        # Move the window to the center
        self.move(x, y)
    
    def showEvent(self, event):
        """Override showEvent to center the window when it's shown"""
        super().showEvent(event)
        self.center()
    
    def load_settings(self):
        """Load settings from app"""
        self.enable_checkbox.setChecked(self.app.settings.get("overlay_enabled", False))
        self.image_path_edit.setText(self.app.settings.get("image_path", ""))
        
        # Set scale factor
        scale_factor = self.app.settings.get("scale_factor", 1.0)
        for button in self.scale_group.buttons():
            if button.property("scale_value") == scale_factor:
                button.setChecked(True)
                break
        
        self.movable_checkbox.setChecked(self.app.settings.get("movable", False))
    
    def toggle_overlay(self):
        """Enable or disable the overlay"""
        self.app.settings["overlay_enabled"] = self.enable_checkbox.isChecked()
        
        if self.enable_checkbox.isChecked():
            self.app.create_overlay()
        else:
            self.app.destroy_overlay()
    
    def update_scale(self):
        """Update scale factor setting"""
        checked_button = self.scale_group.checkedButton()
        if checked_button:
            self.app.settings["scale_factor"] = checked_button.property("scale_value")
            # Update overlay if it exists
            if self.app.overlay_window:
                self.app.overlay_window.update_scale(self.app.settings["scale_factor"])
    
    def update_movable(self):
        """Update movable setting"""
        self.app.settings["movable"] = self.movable_checkbox.isChecked()
        # Update overlay if it exists
        if self.app.overlay_window:
            self.app.overlay_window.update_movable(self.app.settings["movable"])
    
    def browse_image(self):
        """Open file dialog to select image"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Overlay Image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        
        if file_path:
            self.image_path_edit.setText(file_path)
            self.app.settings["image_path"] = file_path
            # Update overlay if it exists
            if self.app.overlay_window:
                self.app.overlay_window.update_image(file_path)
    
    def closeEvent(self, event):
        """Handle window closing"""
        self.app.save_settings()
        super().closeEvent(event)