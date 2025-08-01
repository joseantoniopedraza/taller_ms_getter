# Getter Service

This service fetches tender data from the Mercado Público API and publishes messages to Redis.

## Features

- Fetches tender data from Mercado Público API
- Publishes messages to Redis for further processing
- Comprehensive error handling and logging
- Resilient HTTP requests with timeout handling

## Configuration

Set the following environment variables:

- `REDIS_HOST`: Redis server host (default: localhost)
- `REDIS_PORT`: Redis server port (default: 6379)
- `API_KEY_MERCADO_PUBLICO`: API key for Mercado Público

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python app.py
```

## Testing

### Prerequisites

Install test dependencies:
```bash
pip install -r requirements.txt
```

### Quick Test (No Dependencies Required)

Run a basic structure test:
```bash
python test_simple.py
```

### Full Test Suite (Requires pytest)

Install pytest and run the full test suite:
```bash
# Install pytest if not already installed
pip install pytest pytest-mock pytest-cov responses

# Run all tests with coverage
python run_tests.py

# Run tests in fast mode (no coverage)
python run_tests.py --fast

# Run with pytest directly
pytest tests/ -v
```

### Test Coverage

The test suite includes:
- Unit tests for all functions
- Integration tests for complete workflows
- Error handling tests
- Mocked external dependencies

See `tests/README.md` for detailed test documentation.

## Docker

Build and run with Docker:

```bash
docker build -t getter-service .
docker run -e REDIS_HOST=your-redis-host -e API_KEY_MERCADO_PUBLICO=your-key getter-service
```

## Logging

The service logs to both console and file (`getter_service.log`) with detailed information about:
- Request attempts and responses
- Redis operations
- Error conditions and stack traces
- Processing progress 