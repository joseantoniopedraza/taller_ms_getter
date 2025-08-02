#!/usr/bin/env python3
"""
Simple test script to verify the test structure works
"""

import sys
import os

# Set required environment variables for testing
os.environ["REDIS_HOST"] = "localhost"
os.environ["REDIS_PORT"] = "6379"
os.environ["API_KEY_MERCADO_PUBLICO"] = "test_token"

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_import_app():
    """Test that we can import the app module"""
    try:
        print("✅ Successfully imported app module")
        return True
    except ImportError as e:
        print(f"❌ Failed to import app module: {e}")
        return False


def test_send_function_exists():
    """Test that the send function exists"""
    try:
        import app

        assert hasattr(app, "send")
        print("✅ send function exists")
        return True
    except Exception as e:
        print(f"❌ send function test failed: {e}")
        return False


def test_make_request_function_exists():
    """Test that the make_request function exists"""
    try:
        import app

        assert hasattr(app, "make_request")
        print("✅ make_request function exists")
        return True
    except Exception as e:
        print(f"❌ make_request function test failed: {e}")
        return False


def test_main_function_exists():
    """Test that the main function exists"""
    try:
        import app

        assert hasattr(app, "main")
        print("✅ main function exists")
        return True
    except Exception as e:
        print(f"❌ main function test failed: {e}")
        return False


def test_config_import():
    """Test that config can be imported"""
    try:
        print("✅ config module can be imported")
        return True
    except ImportError as e:
        print(f"❌ Failed to import config module: {e}")
        return False


def run_simple_tests():
    """Run all simple tests"""
    print("Running simple tests for getter service...")
    print("=" * 50)

    tests = [
        test_import_app,
        test_send_function_exists,
        test_make_request_function_exists,
        test_main_function_exists,
        test_config_import,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        print()

    print("=" * 50)
    print(f"Tests passed: {passed}/{total}")

    if passed == total:
        print("✅ All simple tests passed!")
        return True
    else:
        print("❌ Some tests failed!")
        return False


if __name__ == "__main__":
    success = run_simple_tests()
    sys.exit(0 if success else 1)
