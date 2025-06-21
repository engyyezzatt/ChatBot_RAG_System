#!/usr/bin/env python3
"""
Test script to directly test the Python backend
This helps isolate whether the issue is with the .NET API or the Python backend
"""

import requests
import json
import time

def test_python_backend():
    """Test the Python backend directly"""
    base_url = "http://localhost:8000"
    
    print("🔍 Testing Python Backend Directly")
    print("=" * 50)
    
    # Test 1: Health check
    print("1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Health check passed")
            print(f"   Status: {health_data.get('status', 'unknown')}")
            print(f"   Vector Store Status: {health_data.get('vector_store_status', 'unknown')}")
        else:
            print(f"❌ Health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test 2: Chat endpoint
    print("\n2. Testing chat endpoint...")
    try:
        payload = {
            "question": "What is the company leave policy?"
        }
        
        print(f"   Sending request to {base_url}/chat")
        print(f"   Payload: {json.dumps(payload, indent=2)}")
        
        start_time = time.time()
        response = requests.post(
            f"{base_url}/chat",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        end_time = time.time()
        
        print(f"   Response received in {end_time - start_time:.2f} seconds")
        print(f"   Status code: {response.status_code}")
        
        if response.status_code == 200:
            chat_data = response.json()
            print(f"✅ Chat request successful")
            print(f"   Response: {chat_data.get('response', '')[:100]}...")
            print(f"   Sources: {chat_data.get('sources', [])}")
            return True
        else:
            print(f"❌ Chat request failed")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"❌ Chat request timed out after 60 seconds")
        return False
    except Exception as e:
        print(f"❌ Chat request failed: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Python Backend Direct Test")
    print("=" * 50)
    print("This test bypasses the .NET API and tests the Python backend directly.")
    print("If this fails, the issue is with the Python backend.")
    print("If this passes, the issue is with the .NET API communication.")
    print()
    
    success = test_python_backend()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ Python backend is working correctly!")
        print("💡 The issue might be with the .NET API communication.")
    else:
        print("❌ Python backend has issues!")
        print("💡 Please check:")
        print("   1. Is the Python backend running? (python -m uvicorn app.main:app --reload)")
        print("   2. Is it running on http://localhost:8000?")
        print("   3. Are there any error messages in the Python backend console?")
    
    print("=" * 50)

if __name__ == "__main__":
    main() 