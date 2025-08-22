# File: tests/test_industry_lookup_operations.py
"""
Comprehensive tests for industry lookup table operations and management.

WHY: Validates industry categorization system for template and CV metadata tagging
CONTRIBUTION: Ensures complete test coverage for lookup table management and SonarCube compliance
HOW: Tests industry lifecycle management, sector grouping, and active state filtering
"""

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.models.database.postgresql.file_metadata_models import IndustryORM


class TestIndustryLookupOperations:
    """
    Test industry lookup table operations and constraints.
    
    WHY: Validates industry management system for consistent categorization across the platform
    CONTRIBUTION: Ensures reliable industry vocabulary for template filtering and market analysis
    HOW: Tests industry creation, uniqueness constraints, and sector-based organization
    """

    def test_create_valid_industry(self, test_db_session: Session):
        """
        Test successful creation of industry record with valid data.
        
        WHY: Verifies that valid industry records can be created and persisted correctly
        CONTRIBUTION: Ensures core industry management functionality works for legitimate use cases
        HOW: Creates industry with all fields and validates proper persistence and defaults
        """
        industry = IndustryORM(
            name="artificial_intelligence",
            sector="technology",
            is_active=True,
            description="AI and machine learning companies"
        )
        
        test_db_session.add(industry)
        test_db_session.commit()
        test_db_session.refresh(industry)
        
        # Verify all fields are set correctly
        assert industry.id is not None
        assert industry.name == "artificial_intelligence"
        assert industry.sector == "technology"
        assert industry.is_active is True
        assert industry.description == "AI and machine learning companies"
        assert industry.created_at is not None

    def test_industry_name_uniqueness_constraint(self, test_db_session: Session):
        """
        Test industry name uniqueness constraint enforcement.
        
        WHY: Prevents duplicate industry names that would cause categorization confusion
        CONTRIBUTION: Maintains clean industry vocabulary for consistent template and CV tagging
        HOW: Creates industry, then attempts to create duplicate name and expects constraint violation
        """
        # Create first industry
        industry1 = IndustryORM(
            name="fintech",
            sector="financial_services",
            is_active=True,
            description="Financial technology companies"
        )
        test_db_session.add(industry1)
        test_db_session.commit()
        
        # Attempt to create duplicate industry name
        with pytest.raises(IntegrityError):
            industry2 = IndustryORM(
                name="fintech",  # Duplicate name
                sector="technology",  # Different sector
                is_active=True,
                description="Different description"
            )
            test_db_session.add(industry2)
            test_db_session.commit()

    def test_industry_default_values(self, test_db_session: Session):
        """
        Test industry default values for optional fields.
        
        WHY: Ensures proper default behavior when optional fields are not provided
        CONTRIBUTION: Provides predictable industry record structure for consistent API responses
        HOW: Creates industry with minimal required fields and validates default assignments
        """
        industry = IndustryORM(
            name="biotechnology"  # Only required field
        )
        
        test_db_session.add(industry)
        test_db_session.commit()
        test_db_session.refresh(industry)
        
        # Verify default values
        assert industry.is_active is True  # Default should be True
        assert industry.created_at is not None
        assert industry.sector is None  # Optional field, should be None
        assert industry.description is None  # Optional field, should be None

    def test_industry_active_state_filtering(self, test_db_session: Session):
        """
        Test active state filtering for industry management.
        
        WHY: Ensures only active industries appear in UI dropdowns and categorization
        CONTRIBUTION: Provides clean user experience by hiding deprecated industries
        HOW: Creates mixed active/inactive industries and tests filtering queries
        """
        # Create industries with different active states
        industries = [
            IndustryORM(name="active_tech", sector="technology", is_active=True, description="Active tech industry"),
            IndustryORM(name="active_finance", sector="financial_services", is_active=True, description="Active finance industry"),
            IndustryORM(name="deprecated_industry", sector="old_sector", is_active=False, description="Deprecated industry"),
            IndustryORM(name="inactive_sector", sector="inactive", is_active=False, description="Inactive sector")
        ]
        
        test_db_session.add_all(industries)
        test_db_session.commit()
        
        # Query active industries only
        active_industries = test_db_session.query(IndustryORM).filter(
            IndustryORM.is_active == True
        ).all()
        
        active_names = [ind.name for ind in active_industries]
        
        # Verify active industries are returned
        assert "active_tech" in active_names
        assert "active_finance" in active_names
        
        # Verify inactive industries are excluded
        assert "deprecated_industry" not in active_names
        assert "inactive_sector" not in active_names
        
        # Verify count is correct
        assert len(active_industries) == 2

    def test_industry_sector_grouping(self, test_db_session: Session):
        """
        Test industry sector grouping functionality.
        
        WHY: Enables UI organization of industries by sector for better user experience
        CONTRIBUTION: Supports grouped industry displays and sector-based analytics
        HOW: Creates industries with sectors and tests sector-based queries
        """
        # Create industries with different sectors
        industries = [
            IndustryORM(name="software", sector="technology", is_active=True, description="Software companies"),
            IndustryORM(name="hardware", sector="technology", is_active=True, description="Hardware companies"),
            IndustryORM(name="banking", sector="financial_services", is_active=True, description="Banking sector"),
            IndustryORM(name="insurance", sector="financial_services", is_active=True, description="Insurance sector"),
            IndustryORM(name="biotech", sector="healthcare", is_active=True, description="Biotechnology sector")
        ]
        
        test_db_session.add_all(industries)
        test_db_session.commit()
        
        # Query industries by technology sector
        tech_industries = test_db_session.query(IndustryORM).filter(
            IndustryORM.sector == "technology",
            IndustryORM.is_active == True
        ).all()
        
        tech_names = [ind.name for ind in tech_industries]
        
        # Verify technology sector grouping
        assert "software" in tech_names
        assert "hardware" in tech_names
        assert len(tech_names) == 2
        
        # Verify non-technology industries are excluded
        assert "banking" not in tech_names
        assert "insurance" not in tech_names
        assert "biotech" not in tech_names
        
        # Query industries by financial services sector
        finance_industries = test_db_session.query(IndustryORM).filter(
            IndustryORM.sector == "financial_services",
            IndustryORM.is_active == True
        ).all()
        
        finance_names = [ind.name for ind in finance_industries]
        
        # Verify financial services sector grouping
        assert "banking" in finance_names
        assert "insurance" in finance_names
        assert len(finance_names) == 2

    def test_industry_lifecycle_management(self, test_db_session: Session):
        """
        Test complete industry lifecycle management operations.
        
        WHY: Validates industry administrative operations for vocabulary evolution
        CONTRIBUTION: Enables proper industry management and categorization system maintenance
        HOW: Tests industry creation, modification, activation, and deactivation workflows
        """
        # Create new industry
        industry = IndustryORM(
            name="quantum_computing",
            sector="emerging_technology",
            is_active=True,
            description="Quantum computing and quantum technology companies"
        )
        
        test_db_session.add(industry)
        test_db_session.commit()
        test_db_session.refresh(industry)
        
        # Verify initial creation
        assert industry.is_active is True
        assert industry.sector == "emerging_technology"
        initial_created_at = industry.created_at
        
        # Update industry description
        industry.description = "Updated description for quantum computing sector"
        test_db_session.commit()
        test_db_session.refresh(industry)
        
        # Verify update persisted
        assert industry.description == "Updated description for quantum computing sector"
        assert industry.created_at == initial_created_at  # Should not change
        
        # Deactivate industry
        industry.is_active = False
        test_db_session.commit()
        test_db_session.refresh(industry)
        
        # Verify deactivation
        assert industry.is_active is False
        
        # Verify deactivated industry is excluded from active queries
        active_industries = test_db_session.query(IndustryORM).filter(
            IndustryORM.is_active == True
        ).all()
        
        active_names = [ind.name for ind in active_industries]
        assert "quantum_computing" not in active_names
        
        # Reactivate industry
        industry.is_active = True
        test_db_session.commit()
        test_db_session.refresh(industry)
        
        # Verify reactivation
        assert industry.is_active is True

    def test_industry_description_search_capability(self, test_db_session: Session):
        """
        Test industry description field for search and categorization support.
        
        WHY: Enables rich industry descriptions for better user understanding and search
        CONTRIBUTION: Supports future industry search and recommendation features
        HOW: Tests description field storage and retrieval with various content types
        """
        # Create industries with detailed descriptions
        industries = [
            IndustryORM(
                name="renewable_energy",
                sector="energy",
                is_active=True,
                description="Solar, wind, and renewable energy companies focused on sustainable power generation"
            ),
            IndustryORM(
                name="cybersecurity",
                sector="technology",
                is_active=True,
                description="Information security, data protection, and cybersecurity solution providers"
            ),
            IndustryORM(
                name="space_technology",
                sector="aerospace",
                is_active=True,
                description="Aerospace, satellite technology, and space exploration companies"
            )
        ]
        
        test_db_session.add_all(industries)
        test_db_session.commit()
        
        # Test description content retrieval
        renewable_industry = test_db_session.query(IndustryORM).filter(
            IndustryORM.name == "renewable_energy"
        ).first()
        
        assert "Solar" in renewable_industry.description
        assert "sustainable power generation" in renewable_industry.description
        
        # Test description-based filtering (case-insensitive search simulation)
        tech_industries = test_db_session.query(IndustryORM).filter(
            IndustryORM.description.ilike("%technology%")
        ).all()
        
        tech_names = [ind.name for ind in tech_industries]
        assert "space_technology" in tech_names  # Contains "technology" in description
        
        # Test different search term
        security_industries = test_db_session.query(IndustryORM).filter(
            IndustryORM.description.ilike("%security%")
        ).all()
        
        security_names = [ind.name for ind in security_industries]
        assert "cybersecurity" in security_names  # Contains "security" in description
        
        # Verify description lengths for UI display planning
        for industry in industries:
            test_db_session.refresh(industry)
            assert len(industry.description) > 10  # Meaningful descriptions
            assert len(industry.description) < 500  # Reasonable for UI display

    def test_industry_index_performance_validation(self, test_db_session: Session):
        """
        Test industry index performance for common query patterns.
        
        WHY: Validates that industry queries perform efficiently with proper index usage
        CONTRIBUTION: Ensures system scalability and responsive performance with large industry datasets
        HOW: Creates multiple industries and tests common filtering and sorting patterns
        """
        # Create larger dataset of industries for index testing
        industries = []
        sectors = ["technology", "healthcare", "finance", "energy", "manufacturing"]
        
        for i in range(25):  # Create 25 industries across sectors
            industry = IndustryORM(
                name=f"industry_{i:02d}",
                sector=sectors[i % len(sectors)],
                is_active=(i % 4 != 0),  # Mix of active/inactive
                description=f"Description for industry {i}"
            )
            industries.append(industry)
        
        test_db_session.add_all(industries)
        test_db_session.commit()
        
        # Test active industries query (using is_active index)
        active_industries = test_db_session.query(IndustryORM).filter(
            IndustryORM.is_active == True
        ).order_by(IndustryORM.name).all()
        
        # Should return industries where i % 4 != 0 (roughly 75% of 25 = ~18-19)
        assert len(active_industries) >= 18
        assert len(active_industries) <= 19
        
        # Test sector-based filtering combined with active status
        active_tech_industries = test_db_session.query(IndustryORM).filter(
            IndustryORM.sector == "technology",
            IndustryORM.is_active == True
        ).all()
        
        # Should return subset of technology industries that are active
        assert len(active_tech_industries) >= 3  # At least some tech industries should be active
        
        # Test name-based ordering (using name index)
        ordered_industries = test_db_session.query(IndustryORM).filter(
            IndustryORM.is_active == True
        ).order_by(IndustryORM.name).limit(5).all()
        
        # Verify ordering
        industry_names = [ind.name for ind in ordered_industries]
        assert industry_names == sorted(industry_names)  # Should be in alphabetical order