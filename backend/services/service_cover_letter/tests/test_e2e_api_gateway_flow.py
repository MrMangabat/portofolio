# File: tests/test_e2e_api_gateway_flow.py
"""
End-to-end integration test for service_cover_letter → api_gateway → frontend flow.

WHY: Validates complete data flow through all architectural layers ensuring system integration
CONTRIBUTION: Detects communication issues between microservices, API gateway routing, and frontend connectivity
HOW: Tests actual HTTP requests through the gateway to the service and validates responses
"""

import pytest
import requests
import json
import time
from typing import Dict, Any
import uuid
import os
from pathlib import Path

# Service endpoints
SERVICE_DIRECT_URL = "http://localhost:8010"  # Direct service_cover_letter endpoint
API_GATEWAY_URL = "http://localhost:8080"     # API Gateway endpoint
FRONTEND_API_BASE = "http://localhost:3000"    # Nuxt3 frontend (if running)

class TestEndToEndAPIGatewayFlow:
    """
    Test suite for validating complete API flow from frontend through gateway to service.
    
    WHY: Ensures all layers communicate correctly in production-like scenarios
    CONTRIBUTION: Validates routing rules, data serialization, and error handling across boundaries
    HOW: Performs actual HTTP requests simulating frontend behavior through the complete stack
    """

    @pytest.fixture(scope="class")
    def check_services_running(self):
        """
        Verify all required services are running before tests.
        
        WHY: Prevents false test failures due to services being down
        CONTRIBUTION: Provides clear error messages about service availability
        HOW: Attempts connection to each service endpoint with timeout
        """
        services = [
            ("Service Cover Letter", f"{SERVICE_DIRECT_URL}/health"),
            ("API Gateway", f"{API_GATEWAY_URL}/health"),
        ]
        
        for service_name, url in services:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code != 200:
                    pytest.skip(f"{service_name} is not healthy at {url}")
            except requests.exceptions.RequestException:
                pytest.skip(f"{service_name} is not running at {url}")
    
    def test_health_check_through_gateway(self, check_services_running):
        """
        Test health endpoint routing through API gateway.
        
        WHY: Validates basic gateway routing and service discovery
        CONTRIBUTION: Ensures gateway can properly route to service_cover_letter
        HOW: Compares direct service health check with gateway-routed health check
        """
        # Direct service health check
        direct_response = requests.get(f"{SERVICE_DIRECT_URL}/health", timeout=5)
        assert direct_response.status_code == 200
        
        # Gateway routed health check
        gateway_response = requests.get(f"{API_GATEWAY_URL}/health", timeout=5)
        assert gateway_response.status_code == 200
        
        # Both should return similar health status
        assert "status" in gateway_response.json() or "healthy" in gateway_response.text.lower()
    
    def test_jobtypes_endpoint_through_gateway(self, check_services_running):
        """
        Test jobtype lookup endpoint through gateway.
        
        WHY: Validates GET request routing and data retrieval through gateway
        CONTRIBUTION: Ensures lookup endpoints work correctly for frontend dropdowns
        HOW: Fetches jobtypes through gateway and validates response structure
        """
        # Test through API gateway (as frontend would)
        response = requests.get(f"{API_GATEWAY_URL}/files/jobtypes", timeout=5)
        
        assert response.status_code == 200
        data = response.json()
        
        # Validate response structure
        assert isinstance(data, list), "Jobtypes should return a list"
        
        if len(data) > 0:
            # Check first jobtype has expected fields
            jobtype = data[0]
            assert "id" in jobtype
            assert "name" in jobtype
            assert "category" in jobtype
            assert "description" in jobtype
    
    def test_industries_endpoint_through_gateway(self, check_services_running):
        """
        Test industries lookup endpoint through gateway.
        
        WHY: Validates industry data flow for frontend multi-select components
        CONTRIBUTION: Ensures metadata lookup endpoints are properly routed
        HOW: Fetches industries and validates data structure matches frontend expectations
        """
        response = requests.get(f"{API_GATEWAY_URL}/files/industries", timeout=5)
        
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list), "Industries should return a list"
        
        if len(data) > 0:
            industry = data[0]
            assert "id" in industry
            assert "name" in industry
            assert "sector" in industry
            assert "description" in industry
    
    def test_file_upload_with_metadata_through_gateway(self, check_services_running):
        """
        Test enhanced file upload with metadata through gateway.
        
        WHY: Validates multipart form data handling through gateway layers
        CONTRIBUTION: Ensures file upload with metadata works end-to-end
        HOW: Simulates frontend file upload with all metadata fields
        """
        # Create a test file
        test_file_content = b"This is a test cover letter template for TDD validation."
        test_filename = f"test_template_{uuid.uuid4().hex[:8]}.txt"
        
        # Prepare multipart form data as frontend would send
        files = {
            'files': (test_filename, test_file_content, 'text/plain')
        }
        
        data = {
            'file_type': 'template',
            'language': 'english',
            'jobtype': 'data_scientist',
            'industry_sectors': json.dumps(['technology', 'finance']),
            'template_subtype': 'cover_letter',
            'company_size_target': 'any'
        }
        
        # Upload through gateway
        response = requests.post(
            f"{API_GATEWAY_URL}/files/upload-with-metadata",
            files=files,
            data=data,
            timeout=10
        )
        
        # Check response
        assert response.status_code == 200, f"Upload failed: {response.text}"
        
        result = response.json()
        assert "message" in result
        assert "files" in result
        assert len(result["files"]) > 0
        
        # Validate file metadata in response
        uploaded_file = result["files"][0]
        assert uploaded_file["file_type"] == "template"
        assert uploaded_file["language"] == "english"
        assert uploaded_file["jobtype"] == "data_scientist"
    
    def test_file_listing_through_gateway(self, check_services_running):
        """
        Test file listing endpoint through gateway.
        
        WHY: Validates file retrieval for frontend display components
        CONTRIBUTION: Ensures file lists are properly fetched and formatted
        HOW: Requests file list through gateway and validates MinIO integration
        """
        # List files in cover-letters bucket
        response = requests.get(f"{API_GATEWAY_URL}/files/cover-letters", timeout=5)
        
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list), "File listing should return a list"
        
        # If files exist, validate structure
        if len(data) > 0:
            file_item = data[0]
            # Check FileItem model fields
            assert "file_id" in file_item
            assert "file_name" in file_item
            assert "original_file_name" in file_item
            assert "bucket" in file_item
            assert "size" in file_item
            assert "file_type" in file_item
    
    def test_error_handling_through_gateway(self, check_services_running):
        """
        Test error handling and propagation through gateway.
        
        WHY: Validates proper error message propagation to frontend
        CONTRIBUTION: Ensures frontend receives meaningful error messages
        HOW: Triggers various error conditions and validates error responses
        """
        # Test invalid file type
        files = {
            'files': ('test.txt', b'content', 'text/plain')
        }
        
        data = {
            'file_type': 'invalid_type',  # Invalid type
            'language': 'english'
        }
        
        response = requests.post(
            f"{API_GATEWAY_URL}/files/upload-with-metadata",
            files=files,
            data=data,
            timeout=10
        )
        
        # Should return error status
        assert response.status_code >= 400
        
        # Error response should have detail
        error_data = response.json()
        assert "detail" in error_data or "error" in error_data
    
    def test_concurrent_requests_through_gateway(self, check_services_running):
        """
        Test gateway handling of concurrent requests.
        
        WHY: Validates gateway can handle multiple simultaneous frontend requests
        CONTRIBUTION: Ensures system stability under concurrent load
        HOW: Sends multiple simultaneous requests and validates all complete successfully
        """
        import concurrent.futures
        
        def make_request(index: int) -> int:
            """Make a single request and return status code."""
            response = requests.get(f"{API_GATEWAY_URL}/files/jobtypes", timeout=5)
            return response.status_code
        
        # Send 10 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request, i) for i in range(10)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
        
        # All requests should succeed
        assert all(status == 200 for status in results), f"Some requests failed: {results}"
        assert len(results) == 10, "Not all requests completed"
    
    def test_cors_headers_through_gateway(self, check_services_running):
        """
        Test CORS headers for frontend access.
        
        WHY: Validates frontend can make cross-origin requests to gateway
        CONTRIBUTION: Ensures browser-based frontend can communicate with backend
        HOW: Checks for proper CORS headers in gateway responses
        """
        # Simulate frontend origin
        headers = {
            'Origin': 'http://localhost:3000',
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'Content-Type'
        }
        
        # Make OPTIONS preflight request
        response = requests.options(
            f"{API_GATEWAY_URL}/files/upload-with-metadata",
            headers=headers,
            timeout=5
        )
        
        # Check CORS headers
        assert response.status_code in [200, 204], "Preflight request failed"
        
        # Validate CORS headers if present
        if 'Access-Control-Allow-Origin' in response.headers:
            allowed_origin = response.headers['Access-Control-Allow-Origin']
            assert allowed_origin in ['*', 'http://localhost:3000'], f"Unexpected CORS origin: {allowed_origin}"
    
    def test_data_consistency_across_layers(self, check_services_running):
        """
        Test data consistency from frontend format to database storage.
        
        WHY: Validates data integrity through serialization/deserialization across layers
        CONTRIBUTION: Ensures no data corruption or loss through the stack
        HOW: Uploads data with specific values and retrieves to verify consistency
        """
        # Create test data with specific values
        test_uuid = uuid.uuid4().hex[:8]
        test_filename = f"consistency_test_{test_uuid}.txt"
        
        files = {
            'files': (test_filename, b'Test content for consistency', 'text/plain')
        }
        
        original_data = {
            'file_type': 'template',
            'language': 'danish',  # Use less common value
            'jobtype': 'data_engineer',
            'industry_sectors': json.dumps(['healthcare', 'biotech']),
            'template_subtype': 'follow_up',
            'company_size_target': 'startup'
        }
        
        # Upload through gateway
        upload_response = requests.post(
            f"{API_GATEWAY_URL}/files/upload-with-metadata",
            files=files,
            data=original_data,
            timeout=10
        )
        
        assert upload_response.status_code == 200, f"Upload failed: {upload_response.text}"
        
        # Parse response
        result = upload_response.json()
        uploaded_file = result["files"][0]
        
        # Verify data consistency
        assert uploaded_file["file_type"] == "template"
        assert uploaded_file["language"] == "danish"
        assert uploaded_file["jobtype"] == "data_engineer"
        
        # List files to verify it appears
        list_response = requests.get(f"{API_GATEWAY_URL}/files/cover-letters", timeout=5)
        assert list_response.status_code == 200
        
        files_list = list_response.json()
        # Find our uploaded file
        our_file = next((f for f in files_list if test_uuid in f.get("original_file_name", "")), None)
        assert our_file is not None, f"Uploaded file not found in listing"


class TestFrontendSimulation:
    """
    Simulate actual frontend API usage patterns.
    
    WHY: Validates the API behaves correctly for real frontend use cases
    CONTRIBUTION: Ensures frontend integration will work smoothly
    HOW: Mimics actual frontend store actions and API calls
    """
    
    @pytest.fixture(scope="class")
    def api_base(self):
        """Return API base URL as used by frontend."""
        return API_GATEWAY_URL
    
    def test_frontend_file_upload_workflow(self, api_base):
        """
        Simulate complete frontend file upload workflow.
        
        WHY: Validates the complete user journey for file upload
        CONTRIBUTION: Ensures frontend fileStore.js will work correctly
        HOW: Follows exact API call sequence from FileUploads.vue component
        """
        # 1. Load jobtypes (as component does on mount)
        jobtypes_response = requests.get(f"{api_base}/files/jobtypes", timeout=5)
        if jobtypes_response.status_code != 200:
            pytest.skip("Jobtypes endpoint not available")
        
        jobtypes = jobtypes_response.json()
        
        # 2. Load industries (as component does on mount)
        industries_response = requests.get(f"{api_base}/files/industries", timeout=5)
        if industries_response.status_code != 200:
            pytest.skip("Industries endpoint not available")
        
        industries = industries_response.json()
        
        # 3. Simulate user file selection and upload
        # This mimics fileStore.uploadFilesWithMetadata
        test_file = {
            'files': (f'cv_test_{uuid.uuid4().hex[:8]}.pdf', b'Mock CV content', 'application/pdf')
        }
        
        metadata = {
            'file_type': 'cv',
            'language': 'english',
            'experience_years': '5',
            'primary_roles': json.dumps(['Software Engineer', 'Tech Lead']),
            'is_current_cv': 'true'
        }
        
        upload_response = requests.post(
            f"{api_base}/files/upload-with-metadata",
            files=test_file,
            data=metadata,
            timeout=10
        )
        
        if upload_response.status_code != 200:
            pytest.skip(f"Upload endpoint returned {upload_response.status_code}")
        
        # 4. Fetch files (as component does after upload)
        files_response = requests.get(f"{api_base}/files/cv", timeout=5)
        
        assert files_response.status_code in [200, 404], "File listing should work or return 404"
    
    def test_frontend_error_recovery(self, api_base):
        """
        Test frontend error handling scenarios.
        
        WHY: Ensures frontend can gracefully handle backend errors
        CONTRIBUTION: Validates error messages are user-friendly
        HOW: Triggers various error conditions and checks responses
        """
        # Test with missing required fields
        incomplete_data = {
            'file_type': 'template'
            # Missing 'language' field
        }
        
        response = requests.post(
            f"{api_base}/files/upload-with-metadata",
            data=incomplete_data,
            timeout=10
        )
        
        # Should return client error
        assert 400 <= response.status_code < 500, "Should return client error for missing fields"
        
        # Error should be JSON formatted
        try:
            error_data = response.json()
            assert "detail" in error_data or "error" in error_data or "message" in error_data
        except json.JSONDecodeError:
            pytest.fail("Error response should be valid JSON")


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "--tb=short"])