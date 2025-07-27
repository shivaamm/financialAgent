#!/usr/bin/env python3
"""
Comprehensive Backend Testing for Project Raseed
Tests all API endpoints, database connectivity, and integrations
"""

import requests
import json
import os
import sys
import asyncio
import base64
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# Load environment variables
load_dotenv('/app/frontend/.env')
load_dotenv('/app/backend/.env')

# Get backend URL from frontend env
# BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', "http://localhost:8080")
BACKEND_URL = "https://agentraseedbackend-318169846273.europe-west1.run.app"
API_BASE = f"{BACKEND_URL}/api"

# MongoDB connection details
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'test_database')

class BackendTester:
    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0
        
    def log_result(self, test_name, success, message, details=None):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        result = {
            'test': test_name,
            'status': status,
            'message': message,
            'details': details or {}
        }
        self.results.append(result)
        
        if success:
            self.passed += 1
        else:
            self.failed += 1
            
        print(f"{status}: {test_name} - {message}")
        if details and not success:
            print(f"   Details: {details}")
    
    def test_environment_variables(self):
        """Test that required environment variables are loaded"""
        print("\n=== Testing Environment Variables ===")
        
        # Test REACT_APP_BACKEND_URL
        backend_url = os.environ.get('REACT_APP_BACKEND_URL')
        if backend_url:
            self.log_result(
                "Environment - REACT_APP_BACKEND_URL", 
                True, 
                f"Backend URL loaded: {backend_url}"
            )
        else:
            self.log_result(
                "Environment - REACT_APP_BACKEND_URL", 
                False, 
                "REACT_APP_BACKEND_URL not found"
            )
        
        # Test GOOGLE_GEMINI_KEY
        gemini_key = os.environ.get('GOOGLE_GEMINI_KEY')
        if gemini_key:
            self.log_result(
                "Environment - GOOGLE_GEMINI_KEY", 
                True, 
                f"Gemini API key loaded (length: {len(gemini_key)})"
            )
        else:
            self.log_result(
                "Environment - GOOGLE_GEMINI_KEY", 
                False, 
                "GOOGLE_GEMINI_KEY not found"
            )
        
        # Test MONGO_URL
        mongo_url = os.environ.get('MONGO_URL')
        if mongo_url:
            self.log_result(
                "Environment - MONGO_URL", 
                True, 
                f"MongoDB URL loaded: {mongo_url}"
            )
        else:
            self.log_result(
                "Environment - MONGO_URL", 
                False, 
                "MONGO_URL not found"
            )
    
    async def test_database_connection(self):
        """Test MongoDB connection"""
        print("\n=== Testing Database Connection ===")
        
        try:
            client = AsyncIOMotorClient(MONGO_URL)
            # Test connection
            await client.admin.command('ping')
            
            # Test database access
            db = client[DB_NAME]
            collections = await db.list_collection_names()
            
            self.log_result(
                "Database Connection", 
                True, 
                f"MongoDB connected successfully to {DB_NAME}",
                {"collections": collections}
            )
            
            # Test basic operations
            test_doc = {"test": "connection", "timestamp": datetime.utcnow()}
            result = await db.test_collection.insert_one(test_doc)
            
            if result.inserted_id:
                # Clean up test document
                await db.test_collection.delete_one({"_id": result.inserted_id})
                self.log_result(
                    "Database Operations", 
                    True, 
                    "Database read/write operations working"
                )
            else:
                self.log_result(
                    "Database Operations", 
                    False, 
                    "Failed to insert test document"
                )
            
            client.close()
            
        except Exception as e:
            self.log_result(
                "Database Connection", 
                False, 
                f"Database connection failed: {str(e)}"
            )
    
    def test_api_health_check(self):
        """Test basic API health check"""
        print("\n=== Testing API Health Check ===")
        
        try:
            response = requests.get(f"{API_BASE}/", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                expected_message = "Project Raseed - AI Receipt Management System"
                
                if data.get('message') == expected_message:
                    self.log_result(
                        "API Health Check", 
                        True, 
                        "Root endpoint responding correctly",
                        {"response": data}
                    )
                else:
                    self.log_result(
                        "API Health Check", 
                        False, 
                        f"Unexpected response message: {data.get('message')}"
                    )
            else:
                self.log_result(
                    "API Health Check", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except requests.exceptions.RequestException as e:
            self.log_result(
                "API Health Check", 
                False, 
                f"Request failed: {str(e)}"
            )
    
    def test_status_endpoints(self):
        """Test status creation and retrieval endpoints"""
        print("\n=== Testing Status Endpoints ===")
        
        # Test POST /api/status
        try:
            status_data = {
                "client_name": "Test Client Backend Testing"
            }
            
            response = requests.post(
                f"{API_BASE}/status", 
                json=status_data,
                timeout=10
            )
            
            if response.status_code == 200:
                created_status = response.json()
                
                if 'id' in created_status and 'client_name' in created_status:
                    self.log_result(
                        "POST /api/status", 
                        True, 
                        "Status created successfully",
                        {"created_status": created_status}
                    )
                    
                    # Test GET /api/status
                    get_response = requests.get(f"{API_BASE}/status", timeout=10)
                    
                    if get_response.status_code == 200:
                        statuses = get_response.json()
                        
                        if isinstance(statuses, list) and len(statuses) > 0:
                            # Check if our created status is in the list
                            found_status = any(s.get('id') == created_status['id'] for s in statuses)
                            
                            if found_status:
                                self.log_result(
                                    "GET /api/status", 
                                    True, 
                                    f"Status retrieval working, found {len(statuses)} statuses"
                                )
                            else:
                                self.log_result(
                                    "GET /api/status", 
                                    False, 
                                    "Created status not found in status list"
                                )
                        else:
                            self.log_result(
                                "GET /api/status", 
                                False, 
                                "Status list is empty or not a list"
                            )
                    else:
                        self.log_result(
                            "GET /api/status", 
                            False, 
                            f"HTTP {get_response.status_code}: {get_response.text}"
                        )
                else:
                    self.log_result(
                        "POST /api/status", 
                        False, 
                        "Created status missing required fields"
                    )
            else:
                self.log_result(
                    "POST /api/status", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except requests.exceptions.RequestException as e:
            self.log_result(
                "Status Endpoints", 
                False, 
                f"Request failed: {str(e)}"
            )
    
    def test_receipts_endpoint(self):
        """Test receipts endpoint"""
        print("\n=== Testing Receipts Endpoint ===")
        
        try:
            response = requests.get(f"{API_BASE}/receipts", timeout=10)
            
            if response.status_code == 200:
                receipts = response.json()
                
                if isinstance(receipts, list):
                    self.log_result(
                        "GET /api/receipts", 
                        True, 
                        f"Receipts endpoint working, found {len(receipts)} receipts",
                        {"receipt_count": len(receipts)}
                    )
                else:
                    self.log_result(
                        "GET /api/receipts", 
                        False, 
                        "Receipts response is not a list"
                    )
            else:
                self.log_result(
                    "GET /api/receipts", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except requests.exceptions.RequestException as e:
            self.log_result(
                "GET /api/receipts", 
                False, 
                f"Request failed: {str(e)}"
            )
    
    def test_insights_endpoint(self):
        """Test insights endpoint"""
        print("\n=== Testing Insights Endpoint ===")
        
        try:
            response = requests.get(f"{API_BASE}/insights", timeout=10)
            
            if response.status_code == 200:
                insights = response.json()
                
                if isinstance(insights, list):
                    self.log_result(
                        "GET /api/insights", 
                        True, 
                        f"Insights endpoint working, found {len(insights)} insights",
                        {"insight_count": len(insights)}
                    )
                else:
                    self.log_result(
                        "GET /api/insights", 
                        False, 
                        "Insights response is not a list"
                    )
            else:
                self.log_result(
                    "GET /api/insights", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except requests.exceptions.RequestException as e:
            self.log_result(
                "GET /api/insights", 
                False, 
                f"Request failed: {str(e)}"
            )
    
    def test_dashboard_endpoint(self):
        """Test dashboard endpoint"""
        print("\n=== Testing Dashboard Endpoint ===")
        
        try:
            response = requests.get(f"{API_BASE}/dashboard", timeout=10)
            
            if response.status_code == 200:
                dashboard = response.json()
                
                required_fields = ['total_receipts', 'total_spending', 'category_breakdown', 'recent_receipts', 'insights']
                missing_fields = [field for field in required_fields if field not in dashboard]
                
                if not missing_fields:
                    self.log_result(
                        "GET /api/dashboard", 
                        True, 
                        "Dashboard endpoint working with all required fields",
                        {
                            "total_receipts": dashboard.get('total_receipts'),
                            "total_spending": dashboard.get('total_spending'),
                            "categories": len(dashboard.get('category_breakdown', {}))
                        }
                    )
                else:
                    self.log_result(
                        "GET /api/dashboard", 
                        False, 
                        f"Dashboard missing required fields: {missing_fields}"
                    )
            else:
                self.log_result(
                    "GET /api/dashboard", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except requests.exceptions.RequestException as e:
            self.log_result(
                "GET /api/dashboard", 
                False, 
                f"Request failed: {str(e)}"
            )
    
    def test_wallet_passes_endpoint(self):
        """Test wallet passes endpoint"""
        print("\n=== Testing Wallet Passes Endpoint ===")
        
        try:
            response = requests.get(f"{API_BASE}/wallet-passes", timeout=10)
            
            if response.status_code == 200:
                passes = response.json()
                
                if isinstance(passes, list):
                    self.log_result(
                        "GET /api/wallet-passes", 
                        True, 
                        f"Wallet passes endpoint working, found {len(passes)} passes",
                        {"pass_count": len(passes)}
                    )
                else:
                    self.log_result(
                        "GET /api/wallet-passes", 
                        False, 
                        "Wallet passes response is not a list"
                    )
            else:
                self.log_result(
                    "GET /api/wallet-passes", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except requests.exceptions.RequestException as e:
            self.log_result(
                "GET /api/wallet-passes", 
                False, 
                f"Request failed: {str(e)}"
            )
    
    def test_gemini_integration_setup(self):
        """Test Gemini integration setup (without making API calls)"""
        print("\n=== Testing Gemini Integration Setup ===")
        
        try:
            # Import the ReceiptAnalyzer to test initialization
            sys.path.append('/app/backend')
            from server import ReceiptAnalyzer
            
            # Try to initialize the analyzer
            analyzer = ReceiptAnalyzer()
            
            if analyzer.api_key:
                self.log_result(
                    "Gemini Integration Setup", 
                    True, 
                    "ReceiptAnalyzer initialized successfully with API key"
                )
            else:
                self.log_result(
                    "Gemini Integration Setup", 
                    False, 
                    "ReceiptAnalyzer initialized but no API key found"
                )
                
        except ValueError as e:
            if "GOOGLE_GEMINI_KEY not found" in str(e):
                self.log_result(
                    "Gemini Integration Setup", 
                    False, 
                    "GOOGLE_GEMINI_KEY environment variable not found"
                )
            else:
                self.log_result(
                    "Gemini Integration Setup", 
                    False, 
                    f"ReceiptAnalyzer initialization failed: {str(e)}"
                )
        except Exception as e:
            self.log_result(
                "Gemini Integration Setup", 
                False, 
                f"Unexpected error during Gemini setup: {str(e)}"
            )
    
    def test_error_handling(self):
        """Test error handling for invalid requests"""
        print("\n=== Testing Error Handling ===")
        
        # Test invalid endpoint
        try:
            response = requests.get(f"{API_BASE}/invalid-endpoint", timeout=10)
            
            if response.status_code == 404:
                self.log_result(
                    "Error Handling - Invalid Endpoint", 
                    True, 
                    "404 error correctly returned for invalid endpoint"
                )
            else:
                self.log_result(
                    "Error Handling - Invalid Endpoint", 
                    False, 
                    f"Expected 404, got {response.status_code}"
                )
        except requests.exceptions.RequestException as e:
            self.log_result(
                "Error Handling - Invalid Endpoint", 
                False, 
                f"Request failed: {str(e)}"
            )
        
        # Test invalid receipt ID
        try:
            response = requests.get(f"{API_BASE}/receipts/invalid-id", timeout=10)
            
            if response.status_code == 404:
                self.log_result(
                    "Error Handling - Invalid Receipt ID", 
                    True, 
                    "404 error correctly returned for invalid receipt ID"
                )
            else:
                self.log_result(
                    "Error Handling - Invalid Receipt ID", 
                    False, 
                    f"Expected 404, got {response.status_code}"
                )
        except requests.exceptions.RequestException as e:
            self.log_result(
                "Error Handling - Invalid Receipt ID", 
                False, 
                f"Request failed: {str(e)}"
            )
        
        # Test invalid POST data
        try:
            response = requests.post(
                f"{API_BASE}/status", 
                json={"invalid": "data"},
                timeout=10
            )
            
            if response.status_code in [400, 422]:  # Bad Request or Unprocessable Entity
                self.log_result(
                    "Error Handling - Invalid POST Data", 
                    True, 
                    f"Error correctly returned for invalid POST data (HTTP {response.status_code})"
                )
            else:
                self.log_result(
                    "Error Handling - Invalid POST Data", 
                    False, 
                    f"Expected 400/422, got {response.status_code}"
                )
        except requests.exceptions.RequestException as e:
            self.log_result(
                "Error Handling - Invalid POST Data", 
                False, 
                f"Request failed: {str(e)}"
            )
    
    async def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting Project Raseed Backend Testing")
        print(f"Backend URL: {BACKEND_URL}")
        print(f"API Base: {API_BASE}")
        print("=" * 60)
        
        # Run tests
        self.test_environment_variables()
        await self.test_database_connection()
        self.test_api_health_check()
        self.test_status_endpoints()
        self.test_receipts_endpoint()
        self.test_insights_endpoint()
        self.test_dashboard_endpoint()
        self.test_wallet_passes_endpoint()
        self.test_gemini_integration_setup()
        self.test_error_handling()
        
        # Print summary
        print("\n" + "=" * 60)
        print("🏁 TESTING SUMMARY")
        print("=" * 60)
        print(f"✅ PASSED: {self.passed}")
        print(f"❌ FAILED: {self.failed}")
        print(f"📊 TOTAL:  {self.passed + self.failed}")
        
        if self.failed == 0:
            print("\n🎉 ALL TESTS PASSED! Backend is working correctly.")
        else:
            print(f"\n⚠️  {self.failed} test(s) failed. Check the details above.")
        
        return self.failed == 0

def main():
    """Main test runner"""
    tester = BackendTester()
    
    # Run async tests
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        success = loop.run_until_complete(tester.run_all_tests())
        return 0 if success else 1
    finally:
        loop.close()

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)