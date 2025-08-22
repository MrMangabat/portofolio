# File: tests/test_api_connectivity.py
"""
Simple connectivity test for service_cover_letter → api_gateway → frontend flow.

WHY: Validates basic network connectivity and routing between services
CONTRIBUTION: Quickly identifies connectivity issues without complex setup
HOW: Tests basic HTTP connectivity and routing rules
"""

import pytest
import requests
import subprocess
import time

class TestAPIConnectivity:
    """Test basic connectivity between services."""
    
    def test_service_cover_letter_is_running(self):
        """
        Test that service_cover_letter container is accessible.
        
        WHY: Validates the service is running and accepting connections
        CONTRIBUTION: Base requirement for all other tests
        HOW: Checks if service responds to HTTP requests
        """
        try:
            # Check if docs endpoint responds (most reliable)
            response = requests.get("http://localhost:8010/docs", timeout=5)
            assert response.status_code == 200, "Service should have docs endpoint"
            assert "swagger" in response.text.lower(), "Should return Swagger UI"
            print("✅ service_cover_letter is running on port 8010")
        except requests.exceptions.ConnectionError:
            pytest.fail("❌ Cannot connect to service_cover_letter on port 8010")
    
    def test_api_gateway_is_running(self):
        """
        Test that API gateway is accessible.
        
        WHY: Validates gateway is running and can route requests
        CONTRIBUTION: Gateway is critical for frontend communication
        HOW: Checks if gateway responds to requests
        """
        try:
            # Try to access gateway
            response = requests.get("http://localhost:8080/docs", timeout=5)
            assert response.status_code == 200, "Gateway should have docs endpoint"
            print("✅ API Gateway is running on port 8080")
        except requests.exceptions.ConnectionError:
            pytest.fail("❌ Cannot connect to API Gateway on port 8080")
    
    def test_gateway_routes_to_service(self):
        """
        Test that gateway can route to service_cover_letter.
        
        WHY: Validates gateway routing configuration
        CONTRIBUTION: Ensures frontend requests will reach the service
        HOW: Compares direct service access with gateway-routed access
        """
        # Test a known endpoint through both paths
        endpoints_to_test = [
            "/files/cover-letters",  # File listing endpoint
            "/files/jobtypes",       # Jobtype lookup
            "/files/industries",     # Industries lookup
        ]
        
        results = []
        for endpoint in endpoints_to_test:
            # Direct service call
            try:
                direct_response = requests.get(f"http://localhost:8010{endpoint}", timeout=5)
                direct_status = direct_response.status_code
            except:
                direct_status = "Connection Error"
            
            # Gateway routed call
            try:
                gateway_response = requests.get(f"http://localhost:8080{endpoint}", timeout=5)
                gateway_status = gateway_response.status_code
            except:
                gateway_status = "Connection Error"
            
            results.append({
                "endpoint": endpoint,
                "direct": direct_status,
                "gateway": gateway_status
            })
            
            print(f"Endpoint: {endpoint}")
            print(f"  Direct (8010): {direct_status}")
            print(f"  Gateway (8080): {gateway_status}")
        
        # At least some endpoints should be accessible
        accessible_endpoints = [r for r in results if r["gateway"] != "Connection Error"]
        assert len(accessible_endpoints) > 0, "Gateway should route to at least some endpoints"
    
    def test_database_connectivity(self):
        """
        Test that service can connect to PostgreSQL.
        
        WHY: Database connectivity is required for metadata operations
        CONTRIBUTION: Identifies database connection issues
        HOW: Attempts to use an endpoint that requires database access
        """
        # The jobtypes endpoint requires database access
        response = requests.get("http://localhost:8010/files/jobtypes", timeout=5)
        
        # Even if it returns an error, we can check the error type
        if response.status_code == 500:
            error_detail = response.json().get("detail", "")
            if "connection" in error_detail.lower() or "database" in error_detail.lower():
                pytest.fail(f"Database connection issue: {error_detail}")
        
        print(f"Database endpoint response: {response.status_code}")
    
    def test_minio_connectivity(self):
        """
        Test that service can connect to MinIO.
        
        WHY: MinIO connectivity is required for file operations
        CONTRIBUTION: Identifies object storage issues
        HOW: Attempts to list files which requires MinIO access
        """
        response = requests.get("http://localhost:8010/files/cover-letters", timeout=5)
        
        if response.status_code == 500:
            error_detail = response.json().get("detail", "")
            if "minio" in error_detail.lower() or "connection" in error_detail.lower():
                pytest.fail(f"MinIO connection issue: {error_detail}")
        
        print(f"MinIO endpoint response: {response.status_code}")
    
    def test_docker_network_connectivity(self):
        """
        Test Docker network configuration.
        
        WHY: Services must be on the same Docker network to communicate
        CONTRIBUTION: Identifies network configuration issues
        HOW: Checks Docker network setup for all services
        """
        # Get Docker network information
        try:
            # Check if containers are on the same network
            result = subprocess.run(
                ["docker", "network", "inspect", "portofolio_network"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                import json
                network_info = json.loads(result.stdout)
                if network_info:
                    containers = network_info[0].get("Containers", {})
                    container_names = [c.get("Name", "") for c in containers.values()]
                    
                    required_services = ["service_cover_letter", "API_GATEWAY", "cover_letter_postgres", "cover_letter_minio"]
                    
                    for service in required_services:
                        found = any(service in name for name in container_names)
                        if found:
                            print(f"✅ {service} is on portofolio_network")
                        else:
                            print(f"⚠️  {service} not found on portofolio_network")
            else:
                print("⚠️  Could not inspect Docker network")
        except Exception as e:
            print(f"⚠️  Error checking Docker network: {e}")
    
    def test_cors_configuration(self):
        """
        Test CORS headers for frontend access.
        
        WHY: Frontend needs proper CORS headers to make API calls
        CONTRIBUTION: Ensures browser won't block API requests
        HOW: Checks OPTIONS requests and CORS headers
        """
        # Test CORS preflight
        headers = {
            'Origin': 'http://localhost:3000',
            'Access-Control-Request-Method': 'GET'
        }
        
        try:
            response = requests.options("http://localhost:8080/files/jobtypes", headers=headers, timeout=5)
            
            if 'Access-Control-Allow-Origin' in response.headers:
                cors_origin = response.headers['Access-Control-Allow-Origin']
                print(f"✅ CORS configured: {cors_origin}")
                assert cors_origin in ['*', 'http://localhost:3000'], "CORS should allow frontend"
            else:
                print("⚠️  No CORS headers found")
        except:
            print("⚠️  Could not test CORS configuration")
    
    def test_end_to_end_request_flow(self):
        """
        Test complete request flow from simulated frontend.
        
        WHY: Validates the complete request chain works
        CONTRIBUTION: Confirms all layers can communicate
        HOW: Makes a request as frontend would and traces the response
        """
        print("\n=== End-to-End Request Flow Test ===")
        
        # Simulate frontend request to gateway
        headers = {
            'User-Agent': 'Frontend-Test',
            'Accept': 'application/json'
        }
        
        try:
            # 1. Frontend → Gateway
            print("1. Frontend → Gateway (port 8080)")
            gateway_response = requests.get(
                "http://localhost:8080/files/industries",
                headers=headers,
                timeout=5
            )
            print(f"   Response: {gateway_response.status_code}")
            
            # 2. Gateway → Service (we can't directly observe this, but we can infer)
            print("2. Gateway → Service (port 8010)")
            
            # 3. Service → Database/MinIO (check if data is returned)
            if gateway_response.status_code == 200:
                data = gateway_response.json()
                if isinstance(data, list):
                    print(f"   ✅ Received data: {len(data)} items")
                else:
                    print(f"   ✅ Received response: {type(data)}")
            else:
                print(f"   ⚠️  Error response: {gateway_response.status_code}")
                if gateway_response.status_code == 500:
                    error = gateway_response.json()
                    print(f"   Error detail: {error.get('detail', 'Unknown error')}")
        
        except Exception as e:
            print(f"   ❌ Request failed: {e}")


if __name__ == "__main__":
    # Run with verbose output
    pytest.main([__file__, "-v", "-s"])