#!/usr/bin/env python3
"""
SmartContent AI - Backend Runner
Simple script to run the backend API server
"""

import sys
import os
import subprocess
import time

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "fastapi==0.104.1",
            "uvicorn[standard]==0.24.0", 
            "pydantic==2.5.0",
            "structlog==23.2.0",
            "prometheus-client==0.19.0",
            "python-dotenv==1.0.0"
        ])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        sys.exit(1)

def run_server():
    """Run the FastAPI server"""
    print("🚀 Starting SmartContent AI Backend...")
    print("📍 Server will be available at: http://localhost:8000")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/health")
    print("\n" + "="*50)
    
    # Change to backend directory
    os.chdir("backend")
    
    try:
        # Run uvicorn server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload",
            "--log-level", "info"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")

def main():
    """Main function"""
    print("🎯 SmartContent AI - Backend Server")
    print("=" * 40)
    
    check_python_version()
    install_dependencies()
    
    print("\n⚠️  Note: This is a demo version with mock data")
    print("🔑 Add real API keys to .env file for full functionality")
    print("\nPress Ctrl+C to stop the server\n")
    
    time.sleep(2)
    run_server()

if __name__ == "__main__":
    main()