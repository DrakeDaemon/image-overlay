import sys
import json
import os
from PyQt6.QtWidgets import QApplication
from main_window import MainWindow

class ImageOverlayApp:
    def __init__(self):
        self.settings = self.load_settings()
        self.main_window = None
        self.overlay_window = None
        
    def load_settings(self):
        """Load application settings from JSON file"""
        default_settings = {
            "image_path": "assets/default_overlay.png",
            "overlay_enabled": False,
            "scale_factor": 1.0,
            "movable": False,
            "position_x": 100,
            "position_y": 100
        }
        
        try:
            if os.path.exists("config/settings.json"):
                with open("config/settings.json", "r") as f:
                    loaded_settings = json.load(f)
                    # Merge with defaults to ensure all settings exist
                    for key in default_settings:
                        if key not in loaded_settings:
                            loaded_settings[key] = default_settings[key]
                    return loaded_settings
        except Exception as e:
            print(f"Error loading settings: {e}")
            
        return default_settings
    
    def save_settings(self):
        """Save current settings to JSON file"""
        try:
            os.makedirs("config", exist_ok=True)
            with open("config/settings.json", "w") as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def create_overlay(self):
        """Create the overlay window"""
        from overlay_window import OverlayWindow
        
        if self.overlay_window is None:
            self.overlay_window = OverlayWindow(
                self.settings["image_path"],
                self.settings["scale_factor"],
                self.settings["movable"],
                self.settings["position_x"],
                self.settings["position_y"],
                self.update_position_callback
            )
            self.overlay_window.show()
    
    def destroy_overlay(self):
        """Destroy the overlay window"""
        if self.overlay_window:
            self.overlay_window.close()
            self.overlay_window = None
    
    def update_position_callback(self, x, y):
        """Callback to update position in settings"""
        self.settings["position_x"] = x
        self.settings["position_y"] = y
        self.save_settings()
    
    def run(self):
        """Start the application"""
        app = QApplication(sys.argv)
        self.main_window = MainWindow(self)
        self.main_window.show()
        
        # Create overlay if it should be enabled at startup
        if self.settings.get("overlay_enabled", False):
            self.create_overlay()
        
        # Start the event loop
        result = app.exec()
        
        # Save settings when closing
        self.save_settings()
        
        return result

if __name__ == "__main__":
    app = ImageOverlayApp()
    sys.exit(app.run())