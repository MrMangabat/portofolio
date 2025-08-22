#!/usr/bin/env python3
"""
Test runner script for file metadata management system.

WHY: Provides convenient test execution with coverage reporting for SonarCube integration
CONTRIBUTION: Enables quick validation of test suite and coverage metrics during development
HOW: Executes pytest with appropriate configuration and generates coverage reports
"""

import subprocess
import sys
from pathlib import Path


def run_tests():
    """
    Execute the test suite with coverage reporting.
    
    WHY: Centralizes test execution configuration and ensures consistent reporting format
    CONTRIBUTION: Provides standardized test execution for development and CI/CD pipelines
    HOW: Runs pytest with coverage configuration matching SonarCube requirements
    """
    
    # Ensure we're in the correct directory
    project_root = Path(__file__).parent
    
    # Pytest command with coverage - External testing approach
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",
        "--tb=short", 
        "--cov=src/models/database/postgresql/file_metadata_models",
        "--cov-report=xml:coverage.xml",
        "--cov-report=html:htmlcov",
        "--cov-report=term-missing",
        "--cov-fail-under=85",
        "--disable-warnings"
    ]
    
    print("🧪 Running file metadata test suite...")
    print(f"📁 Working directory: {project_root}")
    print(f"🔧 Command: {' '.join(cmd)}")
    print("=" * 80)
    
    try:
        # Run tests
        result = subprocess.run(
            cmd,
            cwd=project_root,
            check=False,
            text=True,
            capture_output=False
        )
        
        print("=" * 80)
        
        if result.returncode == 0:
            print("✅ All tests passed!")
            print("📊 Coverage report generated: htmlcov/index.html")
            print("📋 XML coverage report: coverage.xml")
        else:
            print("❌ Some tests failed or coverage below threshold")
            return result.returncode
            
    except FileNotFoundError:
        print("❌ Error: pytest not found. Install with: pip install pytest pytest-cov")
        return 1
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return 1
    
    return result.returncode


if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)