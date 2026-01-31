#!/usr/bin/env python3
"""
SmartContent AI - API Test Client
Test the running API endpoints
"""

import requests
import json
import time

def test_api():
    """Test the SmartContent AI API"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing SmartContent AI API")
    print("=" * 40)
    
    try:
        # Test health endpoint
        print("1️⃣ Testing health endpoint...")
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Status: {response.json()['status']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
        
        # Test root endpoint
        print("\n2️⃣ Testing root endpoint...")
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Root endpoint works")
            data = response.json()
            print(f"   Message: {data['message']}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
        
        # Test dashboard endpoint
        print("\n3️⃣ Testing dashboard endpoint...")
        response = requests.get(f"{base_url}/api/v1/dashboard")
        if response.status_code == 200:
            print("✅ Dashboard endpoint works")
            data = response.json()
            print(f"   Content generated: {data['overview']['content_generated']}")
            print(f"   Engagement rate: {data['overview']['avg_engagement_rate']}")
        else:
            print(f"❌ Dashboard endpoint failed: {response.status_code}")
        
        # Test content generation
        print("\n4️⃣ Testing content generation...")
        content_request = {
            "prompt": "Create a LinkedIn post about the benefits of AI in content creation",
            "content_type": "social_post",
            "platform": "linkedin"
        }
        
        response = requests.post(
            f"{base_url}/api/v1/content/generate",
            json=content_request
        )
        
        if response.status_code == 200:
            print("✅ Content generation works")
            data = response.json()
            print(f"   Content ID: {data['content_id']}")
            print(f"   Quality score: {data['quality_score']}")
            print(f"   Generated text preview: {data['generated_text'][:100]}...")
        else:
            print(f"❌ Content generation failed: {response.status_code}")
        
        # Test analytics
        print("\n5️⃣ Testing analytics endpoint...")
        response = requests.get(f"{base_url}/api/v1/analytics/performance")
        if response.status_code == 200:
            print("✅ Analytics endpoint works")
            data = response.json()
            print(f"   Total views: {data['summary']['total_views']}")
            print(f"   Avg engagement: {data['summary']['avg_engagement_rate']}")
        else:
            print(f"❌ Analytics endpoint failed: {response.status_code}")
        
        # Test recommendations
        print("\n6️⃣ Testing recommendations endpoint...")
        response = requests.get(f"{base_url}/api/v1/recommendations")
        if response.status_code == 200:
            print("✅ Recommendations endpoint works")
            data = response.json()
            print(f"   Recommendations count: {len(data['recommendations'])}")
            for rec in data['recommendations'][:2]:
                print(f"   • {rec['title']}: {rec['description']}")
        else:
            print(f"❌ Recommendations endpoint failed: {response.status_code}")
        
        print("\n🎉 All API tests completed successfully!")
        print("\n📖 Visit http://localhost:8000/docs for interactive API documentation")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running on http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    # Wait a moment for server to be ready
    print("⏳ Waiting for server to be ready...")
    time.sleep(2)
    
    success = test_api()
    if not success:
        print("\n💡 Make sure the backend server is running:")
        print("   python backend/simple_main.py")