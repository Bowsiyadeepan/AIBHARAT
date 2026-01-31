#!/usr/bin/env python3
"""
SmartContent AI - Demo Launcher
Launch the complete SmartContent AI demo
"""

import webbrowser
import time
import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    """Print welcome banner"""
    print("🚀" + "="*60 + "🚀")
    print("   SMARTCONTENT AI - INTELLIGENT CONTENT PLATFORM")
    print("="*64)
    print("🎯 AI-Powered Content Creation & Distribution Platform")
    print("📊 Real-time Analytics & Performance Tracking")
    print("🤖 Advanced ML Recommendations & Optimization")
    print("⚡ Enterprise-Grade Scalability & Security")
    print("="*64)

def check_server_status():
    """Check if the backend server is running"""
    try:
        import requests
        response = requests.get("http://localhost:8000/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def launch_demo():
    """Launch the SmartContent AI demo"""
    print_banner()
    
    print("\n🔍 Checking system status...")
    
    # Check if server is already running
    if check_server_status():
        print("✅ Backend server is already running")
    else:
        print("⚠️  Backend server not detected")
        print("💡 Make sure to run: python backend/simple_main.py")
        print("   Or check if it's running on a different port")
    
    # Get the demo frontend path
    demo_path = Path(__file__).parent / "demo_frontend.html"
    demo_url = f"file://{demo_path.absolute()}"
    
    print(f"\n🌐 Opening SmartContent AI Demo Dashboard...")
    print(f"📍 Frontend: {demo_url}")
    print(f"🔗 Backend API: http://localhost:8000")
    print(f"📖 API Docs: http://localhost:8000/docs")
    
    # Open the demo in browser
    try:
        webbrowser.open(demo_url)
        print("✅ Demo dashboard opened in browser")
    except Exception as e:
        print(f"❌ Failed to open browser: {e}")
        print(f"💡 Manually open: {demo_url}")
    
    print("\n" + "="*64)
    print("🎉 SMARTCONTENT AI DEMO IS NOW RUNNING!")
    print("="*64)
    print("\n📋 DEMO FEATURES:")
    print("   ✨ AI Content Generation (with mock responses)")
    print("   📊 Real-time Analytics Dashboard")
    print("   🧠 AI-Powered Insights & Recommendations")
    print("   📈 Performance Tracking & Metrics")
    print("   ⚡ Quick Content Creation Tools")
    
    print("\n🔧 TECHNICAL DETAILS:")
    print("   🐍 Backend: FastAPI (Python)")
    print("   🌐 Frontend: HTML5 + TailwindCSS + Chart.js")
    print("   🤖 AI: Mock responses (add real API keys for full functionality)")
    print("   📡 API: RESTful with OpenAPI documentation")
    
    print("\n💡 NEXT STEPS:")
    print("   1. Explore the dashboard and try content generation")
    print("   2. Check the API documentation at /docs")
    print("   3. Add real API keys to .env for full AI functionality")
    print("   4. Deploy to production using the provided guides")
    
    print("\n🚀 Ready to revolutionize your content strategy!")
    print("="*64)

if __name__ == "__main__":
    launch_demo()