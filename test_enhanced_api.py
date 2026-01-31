#!/usr/bin/env python3
"""
SmartContent AI - Enhanced API Test
Test all the new comprehensive endpoints
"""

import requests
import json
import time

def test_enhanced_api():
    """Test the enhanced SmartContent AI API"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing SmartContent AI Enhanced API")
    print("=" * 50)
    
    endpoints_to_test = [
        ("GET", "/health", "Health Check"),
        ("GET", "/", "Root Endpoint"),
        ("GET", "/api/v1/dashboard", "Dashboard Metrics"),
        ("POST", "/api/v1/content/generate", "Content Generation"),
        ("GET", "/api/v1/content", "List Content"),
        ("GET", "/api/v1/content/cnt_001", "Content Details"),
        ("GET", "/api/v1/analytics/performance", "Performance Analytics"),
        ("GET", "/api/v1/analytics/trends", "Trend Analysis"),
        ("GET", "/api/v1/recommendations", "AI Recommendations"),
        ("GET", "/api/v1/campaigns", "Campaign Management"),
        ("GET", "/api/v1/user/profile", "User Profile"),
        ("GET", "/api/v1/system/status", "System Status")
    ]
    
    successful_tests = 0
    total_tests = len(endpoints_to_test)
    
    for method, endpoint, description in endpoints_to_test:
        try:
            print(f"\n🔍 Testing {description}...")
            
            if method == "GET":
                response = requests.get(f"{base_url}{endpoint}", timeout=10)
            elif method == "POST" and "generate" in endpoint:
                # Special case for content generation
                payload = {
                    "prompt": "Create a professional LinkedIn post about the benefits of AI in business",
                    "content_type": "social_post",
                    "platform": "linkedin"
                }
                response = requests.post(f"{base_url}{endpoint}", json=payload, timeout=10)
            else:
                response = requests.post(f"{base_url}{endpoint}", json={}, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ {description} - SUCCESS")
                data = response.json()
                
                # Show some key data points
                if "overview" in data:
                    print(f"   📊 Content generated: {data['overview'].get('content_generated', 'N/A')}")
                elif "generated_text" in data:
                    print(f"   📝 Generated content preview: {data['generated_text'][:80]}...")
                elif "campaigns" in data:
                    print(f"   📈 Total campaigns: {len(data['campaigns'])}")
                elif "recommendations" in data:
                    print(f"   🧠 AI recommendations: {len(data['recommendations'])}")
                elif "status" in data:
                    print(f"   🟢 Status: {data['status']}")
                
                successful_tests += 1
            else:
                print(f"❌ {description} - FAILED (Status: {response.status_code})")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ {description} - CONNECTION ERROR: {e}")
        except Exception as e:
            print(f"❌ {description} - ERROR: {e}")
    
    print("\n" + "=" * 50)
    print(f"🎯 TEST RESULTS: {successful_tests}/{total_tests} endpoints working")
    
    if successful_tests == total_tests:
        print("🎉 ALL TESTS PASSED! SmartContent AI API is fully operational!")
    else:
        print(f"⚠️  {total_tests - successful_tests} endpoints need attention")
    
    print("\n📖 Enhanced API Features:")
    print("   ✨ Comprehensive content management")
    print("   📊 Advanced analytics and trends")
    print("   🤖 AI-powered recommendations")
    print("   📈 Campaign management tools")
    print("   👤 User profile management")
    print("   🔧 System health monitoring")
    
    print(f"\n🌐 Interactive API Documentation: {base_url}/docs")
    print(f"📋 OpenAPI Schema: {base_url}/openapi.json")
    
    return successful_tests == total_tests

if __name__ == "__main__":
    print("⏳ Waiting for enhanced server to be ready...")
    time.sleep(3)
    
    success = test_enhanced_api()
    if success:
        print("\n🚀 SmartContent AI Enhanced API is ready for production!")
    else:
        print("\n🔧 Some endpoints may need configuration or real API keys")