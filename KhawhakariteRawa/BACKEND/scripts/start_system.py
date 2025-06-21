#!/usr/bin/env python3
"""
Cross-platform startup script for Kaiwhakarite Rawa
Handles both backend and frontend server startup with proper error handling
"""

import os
import sys
import time
import signal
import subprocess
import platform
from pathlib import Path
from typing import List, Optional


class Colors:
    """ANSI color codes for console output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_colored(message: str, color: str = Colors.END) -> None:
    """Print colored message to console"""
    print(f"{color}{message}{Colors.END}")


def print_header(title: str) -> None:
    """Print formatted header"""
    print("\n" + "=" * 50)
    print_colored(f"    {title}", Colors.BOLD + Colors.CYAN)
    print("=" * 50)


def check_requirements() -> bool:
    """Check if all required files and dependencies exist"""
    project_root = Path(__file__).parent.parent
    
    # Check required files
    required_files = [
        project_root / "server" / "main.py",
        project_root / "client" / "package.json",
        project_root / "requirements.txt"
    ]
    
    for file_path in required_files:
        if not file_path.exists():
            print_colored(f"❌ Error: {file_path} not found", Colors.RED)
            return False
    
    # Check Python version
    if sys.version_info < (3, 8):
        print_colored("❌ Python 3.8+ required", Colors.RED)
        return False
    
    print_colored("✅ All requirements satisfied", Colors.GREEN)
    return True


def kill_existing_processes() -> None:
    """Kill existing Python and Node processes"""
    print_colored("🔄 Stopping existing servers...", Colors.YELLOW)
    
    system = platform.system().lower()
    
    try:
        if system == "windows":
            subprocess.run(["taskkill", "/f", "/im", "python.exe"], 
                         capture_output=True)
            subprocess.run(["taskkill", "/f", "/im", "node.exe"], 
                         capture_output=True)
        else:
            subprocess.run(["pkill", "-f", "python.*server"], 
                         capture_output=True)
            subprocess.run(["pkill", "-f", "node.*start"], 
                         capture_output=True)
        
        time.sleep(2)
        print_colored("✅ Existing processes stopped", Colors.GREEN)
        
    except Exception as e:
        print_colored(f"⚠️  Warning: Could not stop processes: {e}", 
                     Colors.YELLOW)


def start_backend() -> Optional[subprocess.Popen]:
    """Start the backend server"""
    print_colored("🐍 Starting Backend Server...", Colors.BLUE)
    
    project_root = Path(__file__).parent.parent
    backend_script = project_root / "scripts" / "run_server.py"
    
    try:
        if platform.system().lower() == "windows":
            process = subprocess.Popen(
                [sys.executable, str(backend_script)],
                cwd=project_root,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:
            process = subprocess.Popen(
                [sys.executable, str(backend_script)],
                cwd=project_root
            )
        
        print_colored("✅ Backend server starting...", Colors.GREEN)
        return process
        
    except Exception as e:
        print_colored(f"❌ Failed to start backend: {e}", Colors.RED)
        return None


def start_frontend(mobile_mode: bool = False) -> Optional[subprocess.Popen]:
    """Start the frontend server"""
    mode_text = "Mobile" if mobile_mode else "Desktop"
    print_colored(f"⚛️  Starting Frontend Server ({mode_text})...", 
                 Colors.BLUE)
    
    project_root = Path(__file__).parent.parent
    client_dir = project_root / "client"
    
    try:
        env = os.environ.copy()
        if mobile_mode:
            env["HOST"] = "0.0.0.0"
        
        if platform.system().lower() == "windows":
            process = subprocess.Popen(
                ["npm", "start"],
                cwd=client_dir,
                env=env,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:
            process = subprocess.Popen(
                ["npm", "start"],
                cwd=client_dir,
                env=env
            )
        
        print_colored("✅ Frontend server starting...", Colors.GREEN)
        return process
        
    except Exception as e:
        print_colored(f"❌ Failed to start frontend: {e}", Colors.RED)
        return None


def display_success_info(mobile_mode: bool = False) -> None:
    """Display success information"""
    print_header("🚀 SYSTEM STARTUP COMPLETE!")
    
    host = "0.0.0.0" if mobile_mode else "localhost"
    
    print_colored("✅ Backend API:    http://localhost:8000", Colors.GREEN)
    print_colored("✅ Frontend App:   http://localhost:3000", Colors.GREEN)
    print_colored("✅ API Docs:       http://localhost:8000/docs", Colors.GREEN)
    print_colored("✅ Health Check:   http://localhost:8000/health", Colors.GREEN)
    
    if mobile_mode:
        print_colored("\n📱 Mobile Access:", Colors.CYAN)
        print_colored("   Use your computer's IP address on port 3000", 
                     Colors.CYAN)
    
    print("\n" + "=" * 50)
    print_colored("            🔐 LOGIN CREDENTIALS", Colors.BOLD)
    print("=" * 50)
    print_colored("👑 Admin:     admin@kaiwhakarite.co.nz / admin123", 
                 Colors.BLUE)
    print_colored("👨‍💼 Manager:   kaimahi@kaiwhakarite.co.nz / kaimahi123", 
                 Colors.BLUE)
    print_colored("👤 Staff:     whanau@kaiwhakarite.co.nz / whanau123", 
                 Colors.BLUE)
    print("=" * 50)
    
    print_colored("\n💡 Tips:", Colors.YELLOW)
    print("   - Wait 30-60 seconds for both servers to fully start")
    print("   - Press Ctrl+C to stop this script")
    print("   - Servers will continue running after script exit")


def main():
    """Main startup function"""
    try:
        print_header("Kaiwhakarite Rawa System Launcher")
        
        # Parse command line arguments
        mobile_mode = "--mobile" in sys.argv or "-m" in sys.argv
        
        # Check requirements
        if not check_requirements():
            sys.exit(1)
        
        # Kill existing processes
        kill_existing_processes()
        
        # Start backend
        backend_process = start_backend()
        if not backend_process:
            sys.exit(1)
        
        # Wait for backend to initialize
        print_colored("⏳ Waiting for backend to initialize...", Colors.YELLOW)
        time.sleep(5)
        
        # Start frontend
        frontend_process = start_frontend(mobile_mode)
        if not frontend_process:
            if backend_process:
                backend_process.terminate()
            sys.exit(1)
        
        # Display success information
        display_success_info(mobile_mode)
        
        # Keep script running to catch Ctrl+C
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print_colored("\n🛑 Shutting down servers...", Colors.YELLOW)
            if backend_process:
                backend_process.terminate()
            if frontend_process:
                frontend_process.terminate()
            print_colored("✅ Servers stopped", Colors.GREEN)
            
    except Exception as e:
        print_colored(f"❌ Startup error: {e}", Colors.RED)
        sys.exit(1)


if __name__ == "__main__":
    main() 