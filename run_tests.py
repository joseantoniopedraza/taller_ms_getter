#!/usr/bin/env python3
"""
Test runner script for the getter service
"""

import subprocess
import sys
import os

def run_tests():
    """Run all tests with coverage"""
    print("Running tests for getter service...")
    
    # Run pytest with coverage
    result = subprocess.run([
        sys.executable, "-m", "pytest",
        "--cov=app",
        "--cov-report=term-missing",
        "--cov-report=html:htmlcov",
        "-v"
    ], cwd=os.path.dirname(os.path.abspath(__file__)))
    
    if result.returncode == 0:
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)

def run_tests_fast():
    """Run tests without coverage for faster execution"""
    print("Running tests (fast mode)...")
    
    result = subprocess.run([
        sys.executable, "-m", "pytest",
        "-v"
    ], cwd=os.path.dirname(os.path.abspath(__file__)))
    
    if result.returncode == 0:
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--fast":
        run_tests_fast()
    else:
        run_tests() 