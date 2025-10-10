"""
GUI entry point for Fylum V2.0.0

Launches the desktop application with PyWebView + FastAPI backend
"""

import sys
import threading
import time
from pathlib import Path

try:
    import webview
    from src.api.main import app
    import uvicorn
except ImportError as e:
    print(f"Error: Missing required dependencies for GUI mode.")
    print(f"Please install: pip install fastapi uvicorn pywebview")
    print(f"Details: {e}")
    sys.exit(1)


class FylumGUI:
    """Desktop GUI application wrapper"""
    
    def __init__(self):
        self.api_host = "127.0.0.1"
        self.api_port = 8000
        self.api_url = f"http://{self.api_host}:{self.api_port}"
        self.server_thread = None
    
    def start_api_server(self):
        """Start FastAPI server in background thread"""
        config = uvicorn.Config(
            app,
            host=self.api_host,
            port=self.api_port,
            log_level="warning"
        )
        server = uvicorn.Server(config)
        server.run()
    
    def wait_for_server(self, timeout=10):
        """Wait for API server to be ready"""
        import requests
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                response = requests.get(f"{self.api_url}/api/health")
                if response.status_code == 200:
                    return True
            except requests.exceptions.ConnectionError:
                time.sleep(0.1)
        
        return False
    
    def run(self):
        """Launch the GUI application"""
        print("Starting Fylum GUI...")
        
        # Start API server in background thread
        self.server_thread = threading.Thread(
            target=self.start_api_server,
            daemon=True
        )
        self.server_thread.start()
        
        # Wait for server to be ready
        print("Starting backend server...")
        if not self.wait_for_server():
            print("Error: Failed to start backend server")
            sys.exit(1)
        
        print(f"Backend ready at {self.api_url}")
        
        # TODO: Check if frontend build exists
        # For now, use API docs as placeholder
        frontend_url = f"{self.api_url}/docs"
        
        print("Opening desktop window...")
        
        # Create and show window
        window = webview.create_window(
            title="Fylum - File Organizer",
            url=frontend_url,
            width=1200,
            height=800,
            resizable=True,
            frameless=False,
            easy_drag=True
        )
        
        # Start webview (blocking)
        webview.start(debug=True)


if __name__ == "__main__":
    gui = FylumGUI()
    gui.run()
