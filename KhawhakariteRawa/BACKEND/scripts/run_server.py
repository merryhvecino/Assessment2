#!/usr/bin/env python3
"""
Simple script to run the FastAPI server
"""
import sys
from pathlib import Path
import uvicorn

# Add the parent directory to Python path (where server module is located)
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

# Import the app after adding to path
from server.main import app  # noqa: E402

if __name__ == "__main__":
    
    print("Starting Kaiwhakarite Rawa API Server...")
    print("Server will be available at:")
    print("  - Local: http://localhost:8000")
    print("  - Network: http://192.168.1.4:8000")
    print("API documentation: http://192.168.1.4:8000/docs")
    print("Press Ctrl+C to stop the server")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    ) 