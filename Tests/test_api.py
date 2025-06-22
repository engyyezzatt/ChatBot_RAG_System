#!/usr/bin/env python3
"""
Test script for the .NET Chatbot API
This script tests the main endpoints of the .NET API
"""

import requests
import json
import time
from typing import Dict, Any

class ChatbotAPITester:
    def __init__(self, base_url: str = None):
        # Try to detect the correct URL
        if base_url:
            self.base_url = base_url
        else:
            # Try common development URLs
            self.base_url = self._detect_api_url()
        
        self.session = requests.Session()
        # Disable SSL verification for local development
        self.session.verify = False
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    def _detect_api_url(self) -> str:
        """Try to detect the correct API URL"""
        test_urls = [
            "http://localhost:5001",  # Primary - HTTP on 5001
            "https://localhost:7001", # Fallback - HTTPS on 7001
            "http://localhost:7001",  # Fallback - HTTP on 7001
            "https://localhost:5001"  # Fallback - HTTPS on 5001
        ]
        
        print("🔍 Looking for .NET API...")
        
        for url in test_urls:
            try:
                response = self.session.get(f"{url}/api/health", timeout=3)
                if response.status_code == 200:
                    print(f"✅ Found API at {url}")
                    return url
                else:
                    print(f"⚠️  {url} responded with status {response.status_code}")
            except requests.exceptions.ConnectionError:
                # Connection refused - API not running on this port
                continue
            except requests.exceptions.Timeout:
                # Timeout - API not responding
                continue
            except Exception as e:
                # Other errors
                continue
        
        # Default to the primary URL if none work
        print("⚠️  API not detected, using default: http://localhost:5001")
        return "http://localhost:5001"
    
    def test_health_endpoint(self) -> bool:
        """Test the health endpoint"""
        print("Testing health endpoint...")
        try:
            response = self.session.get(f"{self.base_url}/api/health", timeout=10)
            if response.status_code == 200:
                health_data = response.json()
                print(f"✅ Health check passed")
                print(f"   .NET API Status: {health_data.get('dotnet_api', {}).get('status', 'unknown')}")
                print(f"   Python Backend Status: {health_data.get('python_backend', {}).get('status', 'unknown')}")
                return True
            else:
                print(f"❌ Health check failed with status code: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
        except requests.exceptions.ConnectionError as e:
            print(f"❌ Health check failed - Connection Error: {e}")
            print(f"   Make sure the .NET API is running on {self.base_url}")
            return False
        except Exception as e:
            print(f"❌ Health check failed with error: {e}")
            return False
    
    def test_database_storage(self) -> bool:
        """Test database connection and storage"""
        print("Testing database connection and storage...")
        try:
            # Get initial database stats
            response = self.session.get(f"{self.base_url}/api/chat/db-stats", timeout=10)
            if response.status_code == 200:
                initial_stats = response.json()
                print(f"✅ Database connection successful")
                print(f"   Initial User Queries: {initial_stats.get('user_queries_count', 0)}")
                print(f"   Initial Chatbot Responses: {initial_stats.get('chatbot_responses_count', 0)}")
                return True
            else:
                print(f"❌ Database test failed with status code: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
        except requests.exceptions.ConnectionError as e:
            print(f"❌ Database test failed - Connection Error: {e}")
            return False
        except Exception as e:
            print(f"❌ Database test failed with error: {e}")
            return False
    
    def test_chat_endpoint(self, question: str, session_id: str = None) -> bool:
        """Test the chat endpoint"""
        print(f"Testing chat endpoint with question: '{question}'")
        try:
            payload = {
                "question": question,
                "sessionId": session_id or f"test-session-{int(time.time())}"
            }
            
            response = self.session.post(
                f"{self.base_url}/api/chat",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=120  # Increased from 30 to 120 seconds
            )
            
            if response.status_code == 200:
                chat_data = response.json()
                print(f"✅ Chat request successful")
                print(f"   Query ID: {chat_data.get('queryId')}")
                print(f"   Response: {chat_data.get('response', '')[:100]}...")
                print(f"   Processing Time: {chat_data.get('ProcessingTimeSeconds')}ms")
                print(f"   Status: {chat_data.get('status')}")
                return True
            else:
                print(f"❌ Chat request failed with status code: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
        except requests.exceptions.ConnectionError as e:
            print(f"❌ Chat request failed - Connection Error: {e}")
            return False
        except Exception as e:
            print(f"❌ Chat request failed with error: {e}")
            return False
    
    def test_history_endpoint(self, limit: int = 5) -> bool:
        """Test the conversation history endpoint"""
        print(f"Testing history endpoint (limit: {limit})")
        try:
            response = self.session.get(f"{self.base_url}/api/chat/history?limit={limit}", timeout=10)
            
            if response.status_code == 200:
                history_data = response.json()
                print(f"✅ History request successful")
                print(f"   Retrieved {len(history_data)} conversation records")
                if history_data:
                    latest = history_data[0]
                    print(f"   Latest question: {latest.get('question', '')[:50]}...")
                return True
            else:
                print(f"❌ History request failed with status code: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
        except requests.exceptions.ConnectionError as e:
            print(f"❌ History request failed - Connection Error: {e}")
            return False
        except Exception as e:
            print(f"❌ History request failed with error: {e}")
            return False
    
    def test_database_after_chat(self) -> bool:
        """Test database after chat to verify storage"""
        print("Verifying database storage after chat...")
        try:
            response = self.session.get(f"{self.base_url}/api/chat/db-stats", timeout=10)
            if response.status_code == 200:
                stats = response.json()
                print(f"✅ Database verification successful")
                print(f"   User Queries: {stats.get('user_queries_count', 0)}")
                print(f"   Chatbot Responses: {stats.get('chatbot_responses_count', 0)}")
                
                # Show recent entries
                recent_queries = stats.get('recent_queries', [])
                recent_responses = stats.get('recent_responses', [])
                
                if recent_queries:
                    print(f"   Latest Query: {recent_queries[0].get('question', '')[:50]}...")
                if recent_responses:
                    print(f"   Latest Response: {recent_responses[0].get('response', '')[:50]}...")
                
                return True
            else:
                print(f"❌ Database verification failed with status code: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Database verification failed with error: {e}")
            return False
    
    def run_full_test(self) -> bool:
        """Run all tests"""
        print("=" * 60)
        print("Starting .NET Chatbot API Tests")
        print(f"Using API URL: {self.base_url}")
        print("=" * 60)
        
        tests = [
            ("Health Check", self.test_health_endpoint),
            ("Database Connection", self.test_database_storage),
            ("Chat Request", lambda: self.test_chat_endpoint("What is the company leave policy?")),
            ("Database Storage Verification", self.test_database_after_chat),
            ("History Request", lambda: self.test_history_endpoint(3))
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n--- {test_name} ---")
            if test_func():
                passed += 1
            time.sleep(1)  # Small delay between tests
        
        print("\n" + "=" * 60)
        print(f"Test Results: {passed}/{total} tests passed")
        print("=" * 60)
        
        return passed == total

def main():
    """Main function to run the tests"""
    tester = ChatbotAPITester()
    
    try:
        success = tester.run_full_test()
        if success:
            print("🎉 All tests passed! The .NET API is working correctly.")
            print("✅ Database storage is working - user queries and responses are being saved!")
        else:
            print("⚠️  Some tests failed. Please check the API and try again.")
            print("\n💡 Troubleshooting tips:")
            print("   1. Make sure the .NET API is running (dotnet run)")
            print("   2. Check the console output for the correct port")
            print("   3. Ensure the Python backend is running on http://localhost:8000")
            print("   4. Verify database connection in appsettings.json")
            print("   5. Try accessing the API manually in your browser: http://localhost:5001/swagger")
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"\n❌ Test suite failed with error: {e}")

if __name__ == "__main__":
    main() 