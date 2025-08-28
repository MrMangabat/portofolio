# File: tests/test_corrections_delete_behavior.py
"""
Test corrections CRUD endpoint behavior with proper UUID handling.

WHY: Validates CREATE and DELETE endpoints work with UUID types correctly
CONTRIBUTION: Ensures CRUD operations handle UUID typing properly after migration
HOW: Tests endpoints with real UUID parameters and validates response structures
"""

import pytest
import requests
from uuid import UUID
from src.models.database.postgresql.postgres_models import CorrectionItem, CorrectionType


class TestCorrectionsCRUDBehavior:
    """Test CREATE and DELETE endpoint behavior with UUID parameters."""
    
    BASE_URL = "http://localhost:8010"
    
    # ==================== CREATE/POST Tests ====================
    
    def test_create_correction_with_all_types(self):
        """
        Test POST endpoint creates corrections with UUID response.
        
        WHY: Validates POST endpoint creates corrections and returns UUID
        CONTRIBUTION: Ensures creation works for all correction types
        HOW: Creates corrections of each type and validates UUID generation
        """
        test_cases = [
            {"text": "Python programming", "type": "skill"},
            {"text": "perfectly", "type": "word"},
            {"text": "I am a perfect fit", "type": "sentence"}
        ]
        
        created_ids = []
        
        for test_data in test_cases:
            # Include id field as None (optional)
            correction_data = {
                "id": None,
                "text": test_data["text"],
                "type": test_data["type"]
            }
            
            response = requests.post(
                f"{self.BASE_URL}/corrections",
                json=correction_data,
                headers={"Content-Type": "application/json"}
            )
            
            assert response.status_code == 200, f"Failed to create {test_data['type']}: {response.text}"
            
            created = response.json()
            
            # Validate response structure
            assert "id" in created
            assert "text" in created
            assert "type" in created
            
            # Validate UUID format
            correction_id = created["id"]
            UUID(correction_id)  # Will raise if invalid
            
            # Validate content matches request
            assert created["text"] == test_data["text"]
            assert created["type"] == test_data["type"]
            
            created_ids.append(correction_id)
            print(f"✅ Created {test_data['type']}: {correction_id}")
        
        # Cleanup - delete created test data
        for correction_id in created_ids:
            requests.delete(f"{self.BASE_URL}/corrections/{correction_id}")
    
    def test_create_correction_without_id_field(self):
        """
        Test POST endpoint accepts payload without id field.
        
        WHY: Validates id is truly optional in request payload
        CONTRIBUTION: Ensures backward compatibility with clients not sending id
        HOW: Sends correction data without id field and validates creation
        """
        # Deliberately omit the id field
        correction_data = {
            "text": "Test without ID field",
            "type": "skill"
        }
        
        response = requests.post(
            f"{self.BASE_URL}/corrections",
            json=correction_data,
            headers={"Content-Type": "application/json"}
        )
        
        # Should still work without id field
        if response.status_code != 200:
            print(f"Response: {response.status_code} - {response.text}")
        
        assert response.status_code == 200
        created = response.json()
        
        # Should have generated UUID
        assert "id" in created
        UUID(created["id"])
        
        # Cleanup
        requests.delete(f"{self.BASE_URL}/corrections/{created['id']}")
        print("✅ POST works without id field in request")
    
    def test_create_duplicate_text_allowed(self):
        """
        Test POST allows duplicate text entries.
        
        WHY: Validates business rule that duplicate corrections are allowed
        CONTRIBUTION: Ensures system handles duplicate text entries correctly
        HOW: Creates two corrections with same text and validates both exist
        """
        correction_data = {
            "id": None,
            "text": "Duplicate test skill",
            "type": "skill"
        }
        
        # Create first correction
        response1 = requests.post(
            f"{self.BASE_URL}/corrections",
            json=correction_data
        )
        assert response1.status_code == 200
        created1 = response1.json()
        
        # Create second correction with same text
        response2 = requests.post(
            f"{self.BASE_URL}/corrections",
            json=correction_data
        )
        assert response2.status_code == 200
        created2 = response2.json()
        
        # Should have different UUIDs
        assert created1["id"] != created2["id"]
        assert created1["text"] == created2["text"]
        
        # Cleanup
        requests.delete(f"{self.BASE_URL}/corrections/{created1['id']}")
        requests.delete(f"{self.BASE_URL}/corrections/{created2['id']}")
        print("✅ Duplicate text entries allowed with different UUIDs")
    
    def test_create_returns_uuid_not_integer(self):
        """
        Test POST returns UUID format not integer ID.
        
        WHY: Validates migration from integer to UUID primary keys
        CONTRIBUTION: Ensures UUID migration is complete
        HOW: Creates correction and validates ID is valid UUID format
        """
        correction_data = {
            "id": None,
            "text": "UUID format test",
            "type": "skill"
        }
        
        response = requests.post(
            f"{self.BASE_URL}/corrections",
            json=correction_data
        )
        assert response.status_code == 200
        created = response.json()
        
        correction_id = created["id"]
        
        # Should be valid UUID string
        assert isinstance(correction_id, str)
        assert "-" in correction_id  # UUIDs have hyphens
        assert len(correction_id) == 36  # Standard UUID length
        
        # Should parse as valid UUID
        parsed_uuid = UUID(correction_id)
        assert str(parsed_uuid) == correction_id
        
        # Should NOT be an integer
        try:
            int(correction_id)
            assert False, "ID should not be convertible to integer"
        except ValueError:
            pass  # Expected - UUID strings can't convert to int
        
        # Cleanup
        requests.delete(f"{self.BASE_URL}/corrections/{correction_id}")
        print(f"✅ POST returns proper UUID format: {correction_id}")
    
    def test_create_with_invalid_type_rejected(self):
        """
        Test POST rejects invalid correction types.
        
        WHY: Validates enum type validation is working
        CONTRIBUTION: Ensures only valid correction types are accepted
        HOW: Sends invalid type and validates 422 response
        """
        correction_data = {
            "id": None,
            "text": "Invalid type test",
            "type": "invalid_type"  # Not in enum
        }
        
        response = requests.post(
            f"{self.BASE_URL}/corrections",
            json=correction_data
        )
        
        assert response.status_code == 422
        error = response.json()
        assert "detail" in error
        print("✅ POST properly rejects invalid correction types")
    
    # ==================== DELETE Tests ====================
    
    def test_delete_with_valid_uuid(self):
        """
        Test DELETE endpoint accepts valid UUID and returns deleted object.
        
        WHY: Validates the 422 error fix by ensuring UUIDs are properly accepted
        CONTRIBUTION: Confirms DELETE endpoint works with UUID type instead of int
        HOW: Creates correction, deletes it with UUID, validates response structure
        """
        # First, create a correction to delete
        correction_data = {
            "id": None,  # Include id field as None
            "text": "Test DELETE skill",
            "type": "skill"
        }
        
        create_response = requests.post(
            f"{self.BASE_URL}/corrections",
            json=correction_data,
            headers={"Content-Type": "application/json"}
        )
        
        if create_response.status_code != 200:
            print(f"POST error: {create_response.status_code}")
            print(f"Error detail: {create_response.text}")
        
        assert create_response.status_code == 200
        created_correction = create_response.json()
        correction_id = created_correction["id"]
        
        # Validate it's a proper UUID string
        UUID(correction_id)  # Will raise ValueError if not valid UUID
        
        # Now delete the correction
        delete_response = requests.delete(
            f"{self.BASE_URL}/corrections/{correction_id}",
            headers={"Accept": "application/json"}
        )
        
        # Validate DELETE response
        assert delete_response.status_code == 200
        deleted_correction = delete_response.json()
        
        # Validate response structure
        assert "id" in deleted_correction
        assert "text" in deleted_correction  
        assert "type" in deleted_correction
        
        # Validate response content
        assert deleted_correction["id"] == correction_id
        assert deleted_correction["text"] == "Test DELETE skill"
        assert deleted_correction["type"] == "skill"
        
        # Validate correction is actually deleted
        verify_response = requests.get(f"{self.BASE_URL}/corrections")
        assert verify_response.status_code == 200
        
        remaining_corrections = verify_response.json()
        deleted_ids = [c["id"] for c in remaining_corrections]
        assert correction_id not in deleted_ids
        
        print(f"✅ DELETE endpoint successfully handled UUID: {correction_id}")
    
    def test_delete_with_nonexistent_uuid(self):
        """
        Test DELETE endpoint with non-existent UUID returns 404.
        
        WHY: Validates proper error handling for missing resources
        CONTRIBUTION: Ensures DELETE endpoint has proper validation logic
        HOW: Uses valid UUID format but non-existent ID to test 404 behavior
        """
        # Use a valid UUID format but non-existent ID
        fake_uuid = "00000000-0000-4000-8000-000000000000"
        
        delete_response = requests.delete(
            f"{self.BASE_URL}/corrections/{fake_uuid}",
            headers={"Accept": "application/json"}
        )
        
        assert delete_response.status_code == 404
        error_response = delete_response.json()
        assert "detail" in error_response
        assert "not found" in error_response["detail"].lower()
        
        print(f"✅ DELETE endpoint properly handled non-existent UUID: {fake_uuid}")
    
    def test_delete_with_invalid_uuid_format(self):
        """
        Test DELETE endpoint with invalid UUID format returns 422.
        
        WHY: Validates UUID type validation is working properly
        CONTRIBUTION: Ensures UUID typing prevents invalid input acceptance
        HOW: Sends invalid UUID string and validates 422 response
        """
        invalid_uuid = "not-a-valid-uuid"
        
        delete_response = requests.delete(
            f"{self.BASE_URL}/corrections/{invalid_uuid}",
            headers={"Accept": "application/json"}
        )
        
        # Should get 422 for invalid UUID format
        assert delete_response.status_code == 422
        error_response = delete_response.json()
        assert "detail" in error_response
        
        print(f"✅ DELETE endpoint properly rejected invalid UUID: {invalid_uuid}")
    
    def test_delete_endpoint_uuid_typing_regression(self):
        """
        Regression test for the original 422 error with valid UUIDs.
        
        WHY: Prevents regression of the original issue where valid UUIDs caused 422 errors
        CONTRIBUTION: Ensures UUID typing fix remains functional over time
        HOW: Creates multiple corrections and deletes them to validate UUID handling
        """
        created_corrections = []
        
        # Create multiple corrections
        for i in range(3):
            correction_data = {
                "id": None,  # Include id field as None
                "text": f"Regression test skill {i}",
                "type": "skill"
            }
            
            create_response = requests.post(
                f"{self.BASE_URL}/corrections",
                json=correction_data
            )
            assert create_response.status_code == 200
            created_corrections.append(create_response.json())
        
        # Delete each one - should not get 422 errors
        for correction in created_corrections:
            correction_id = correction["id"]
            
            # Validate UUID format
            UUID(correction_id)
            
            delete_response = requests.delete(
                f"{self.BASE_URL}/corrections/{correction_id}"
            )
            
            # This was the original bug - should NOT be 422
            assert delete_response.status_code != 422
            assert delete_response.status_code == 200
            
            deleted_data = delete_response.json()
            assert deleted_data["id"] == correction_id
        
        print("✅ No regression - all UUIDs processed correctly without 422 errors")


if __name__ == "__main__":
    # Run with verbose output
    pytest.main([__file__, "-v", "-s"])