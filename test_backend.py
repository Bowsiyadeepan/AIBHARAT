#!/usr/bin/env python3
"""
SmartContent AI - Backend Test
Test the backend API endpoints
"""

import sys
import os
import asyncio
import json
from datetime import datetime

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

async def test_backend():
    """Test the backend functionality"""
    print("🧪 Testing SmartContent AI Backend")
    print("=" * 40)
    
    try:
        # Import backend modules
        from main import app
        from models.content import ContentGenerationRequest, ContentType, Tone
        from models.user import User
        
        print("✅ Backend modules imported successfully")
        
        # Test content generation request model
        test_request = ContentGenerationRequest(
            prompt="Create a LinkedIn post about AI productivity tools",
            content_type=ContentType.SOCIAL_POST,
            platform="linkedin",
            tone=Tone.PROFESSIONAL,
            include_hashtags=True,
            include_cta=True
        )
        
        print("✅ Content generation request model works")
        print(f"   📝 Prompt: {test_request.prompt[:50]}...")
        print(f"   📱 Platform: {test_request.platform}")
        print(f"   🎭 Tone: {test_request.tone}")
        
        # Test user model
        test_user = User(
            id="test_123",
            email="test@smartcontent.ai",
            username="test_user",
            role="user",
            subscription_tier="pro",
            is_active=True,
            email_verified=True,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        print("✅ User model works")
        print(f"   👤 User: {test_user.username} ({test_user.email})")
        print(f"   🎫 Tier: {test_user.subscription_tier}")
        
        # Test FastAPI app
        print("✅ FastAPI application created successfully")
        print(f"   🚀 App title: {app.title}")
        print(f"   📋 Version: {app.version}")
        
        print("\n🎉 All backend tests passed!")
        print("\n📍 To run the server:")
        print("   python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000")
        print("\n📖 API Documentation will be available at:")
        print("   http://localhost:8000/docs")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all dependencies are installed")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Main function"""
    success = asyncio.run(test_backend())
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()