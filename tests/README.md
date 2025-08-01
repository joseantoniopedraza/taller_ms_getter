# Tests for Getter Service

This directory contains comprehensive tests for the `app.py` file in the getter service.

## Test Structure

- `test_app.py` - Main test file with unit and integration tests
- `conftest.py` - Pytest configuration and fixtures
- `README.md` - This documentation file

## Test Categories

### Unit Tests
- **TestSendFunction**: Tests for the `send()` function
  - Success case
  - Redis error handling
  - Unexpected error handling

- **TestMakeRequestFunction**: Tests for the `make_request()` function
  - Successful HTTP requests
  - HTTP error handling
  - JSON decode error handling
  - Unexpected error handling

- **TestMainFunction**: Tests for the `main()` function
  - Successful execution
  - Invalid response handling
  - Empty tenders list
  - Individual tender error handling
  - Critical error handling

### Integration Tests
- **TestIntegration**: End-to-end workflow tests
  - Complete workflow from API calls to Redis publishing

## Running Tests

### Prerequisites
Install test dependencies:
```bash
pip install -r requirements.txt
```

### Run all tests with coverage
```bash
python run_tests.py
```

### Run tests in fast mode (no coverage)
```bash
python run_tests.py --fast
```

### Run tests with pytest directly
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test class
pytest tests/test_app.py::TestSendFunction

# Run specific test method
pytest tests/test_app.py::TestSendFunction::test_send_success
```

### Run tests by category
```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration
```

## Test Coverage

The tests cover:
- ✅ All public functions (`send`, `make_request`, `main`)
- ✅ Success scenarios
- ✅ Error handling for all major error types
- ✅ Edge cases (empty responses, invalid data)
- ✅ Integration workflows
- ✅ Logging behavior (disabled during tests)

## Test Data

The tests use mocked data that simulates the real API responses:
- Tenders list with multiple entries
- Individual tender details
- Expected message structure for Redis publishing

## Mocking Strategy

- **Redis**: Mocked to avoid requiring a real Redis instance
- **HTTP Requests**: Mocked to avoid external API calls
- **Configuration**: Environment variables set for testing
- **Logging**: Disabled during tests to avoid cluttered output

## Adding New Tests

When adding new functionality to `app.py`:

1. Add corresponding test methods to the appropriate test class
2. Use the existing fixtures from `conftest.py`
3. Follow the Arrange-Act-Assert pattern
4. Test both success and error scenarios
5. Update this README if adding new test categories 