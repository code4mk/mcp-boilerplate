# Testing Documentation

## Overview

This MCP server project includes a comprehensive test suite with unit tests and integration tests. The test suite uses pytest as the testing framework and includes coverage reporting, fixtures, and custom markers for organizing tests.

### Test Structure

```
tests/
├── __init__.py
├── conftest.py              # Shared pytest configuration
├── fixtures/                # Test fixtures and mocks
│   ├── __init__.py
│   ├── context.py          # Context fixtures
│   └── weather.py          # Weather-related fixtures
├── unit/                    # Unit tests (39 tests)
│   ├── test_elicitation.py
│   ├── test_models.py
│   ├── test_travel_prompts.py
│   ├── test_weather_forecast.py
│   └── test_weather_resource.py
└── integration/             # Integration tests (15 tests)
    ├── test_itinerary_tool.py
    └── test_weather_api.py
```

**Total Tests**: 54 tests
- **Unit Tests**: 39 tests (fast, isolated component testing)
- **Integration Tests**: 15 tests (component interaction testing)

## Quick Start

### Installation

Ensure you have pytest and coverage tools installed:

```bash
# Using uv (recommended)
uv pip install pytest pytest-cov pytest-asyncio

# Using pip
pip install pytest pytest-cov pytest-asyncio
```

### Run All Tests

```bash
pytest
# or with verbose output
pytest tests/ -v
```

## Test Organization

### Test Markers

Tests are organized using pytest markers defined in `pytest.ini`:

- `@pytest.mark.unit` - Unit tests for isolated component testing
- `@pytest.mark.integration` - Integration tests for component interactions
- `@pytest.mark.slow` - Tests that take longer to execute
- `@pytest.mark.skip_ci` - Tests to skip in CI environments

### Test Files

#### Unit Tests

1. **test_models.py** - Tests for data models (ItineraryPreferences, Location, etc.)
2. **test_elicitation.py** - Tests for preference elicitation utilities
3. **test_weather_forecast.py** - Tests for weather forecast utilities
4. **test_weather_resource.py** - Tests for weather resource components
5. **test_travel_prompts.py** - Tests for travel prompt generation

#### Integration Tests

1. **test_itinerary_tool.py** - Tests for itinerary tool integration
2. **test_weather_api.py** - Tests for weather API integration

## Running Tests

### Basic Commands

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with extra verbose output
pytest -vv

# Run quietly (minimal output)
pytest -q
```

### Run Tests by Type

```bash
# Unit tests only (fast, isolated)
pytest tests/unit/ -v
pytest -m unit

# Integration tests only (component interactions)
pytest tests/integration/ -v
pytest -m integration

# Exclude slow tests
pytest -m "not slow"
```

### Run Specific Tests

```bash
# Single test file
pytest tests/unit/test_models.py -v

# Multiple test files
pytest tests/unit/test_models.py tests/unit/test_elicitation.py -v

# Specific test class
pytest tests/unit/test_models.py::TestItineraryPreferences -v

# Specific test method
pytest tests/unit/test_models.py::TestItineraryPreferences::test_valid_preferences -v

# Pattern matching by keyword
pytest -k "elicitation" -v
pytest -k "weather and not api" -v
pytest -k "test_valid and not cancelled"
```

### Run Tests by Path Pattern

```bash
pytest tests/unit/test_*.py
pytest tests/**/test_weather*.py
```

## Coverage

### Basic Coverage Commands

```bash
# Run tests with coverage
pytest --cov=src/mcp_server

# With terminal report
pytest --cov=src/mcp_server --cov-report=term

# With HTML report (opens in browser)
pytest --cov=src/mcp_server --cov-report=html
open htmlcov/index.html
```

### Detailed Coverage

```bash
# Show missing lines in coverage report
pytest --cov=src/mcp_server --cov-report=term-missing

# Coverage for specific module
pytest --cov=src/mcp_server.utils tests/unit/test_weather_forecast.py

# Generate multiple report formats
pytest --cov=src/mcp_server --cov-report=html --cov-report=xml --cov-report=term

# Combine unit tests with coverage
pytest tests/unit/ --cov=src/mcp_server --cov-report=term -v
```

## Output Control

### Verbose and Debug Output

```bash
# Show test names
pytest -v

# Show more details
pytest -vv

# Show print statements from tests
pytest -s

# Show local variables on failure
pytest -l

# Show captured log messages
pytest --log-cli-level=INFO
```

### Custom Log Configuration

The project's `pytest.ini` configures logging:
- Log level: INFO
- Format: `%(asctime)s [%(levelname)8s] %(message)s`
- Date format: `%Y-%m-%d %H:%M:%S`

## Debugging

### Stop on Failures

```bash
# Stop on first failure
pytest -x
pytest --maxfail=1

# Stop after N failures
pytest --maxfail=3
```

### Rerun Failed Tests

```bash
# Run only last failed tests
pytest --lf
pytest --last-failed

# Run failed tests first, then continue with others
pytest --ff
pytest --failed-first
```

### PDB Debugging

```bash
# Drop into debugger on failure
pytest --pdb

# Drop into debugger at start of each test
pytest --trace

# Debug specific test with all output
pytest tests/unit/test_models.py::TestItineraryPreferences::test_valid_preferences -vv -s --pdb
```

## Performance

### Parallel Execution

```bash
# Auto-detect CPU count (requires pytest-xdist)
pytest -n auto

# Specific number of workers
pytest -n 4

# Parallel execution with coverage
pytest -n auto --cov=src/mcp_server --cov-report=html
```

### Duration Reports

```bash
# Show slowest 10 tests
pytest --durations=10

# Show all test durations
pytest --durations=0
```

## Reporting

### Generate Reports for CI/CD

```bash
# JUnit XML report (for CI systems)
pytest --junitxml=report.xml

# JSON report (requires pytest-json-report)
pytest --json-report --json-report-file=report.json

# Multiple report formats
pytest \
  --cov=src/mcp_server \
  --cov-report=xml \
  --cov-report=term \
  --junitxml=test-results.xml \
  -v
```

### List All Markers

```bash
# List all available markers
pytest --markers

# Run with strict marker checking (fails on unknown markers)
pytest --strict-markers
```

## Common Workflows

### Development Workflow

```bash
# Quick feedback: run related unit tests
pytest tests/unit/test_models.py -v

# Debug with print statements
pytest tests/unit/test_models.py -v -s

# Debug failing test with pdb
pytest tests/unit/test_models.py::TestItineraryPreferences::test_custom_days --pdb -x
```

### Pre-Commit Check

```bash
# Run all tests with coverage and stop on failures
pytest --cov=src/mcp_server --cov-report=term-missing --maxfail=5
```

### Quick Sanity Check

```bash
# Fast unit tests only, fail fast
pytest tests/unit/ -v --maxfail=1
```

### Full Quality Check

```bash
# Comprehensive test run with coverage and strict checks
pytest \
  --cov=src/mcp_server \
  --cov-report=html \
  --cov-report=term-missing \
  --strict-markers \
  --maxfail=1 \
  -vv
```

### CI Pipeline

```bash
# Full test suite optimized for CI
pytest \
  --cov=src/mcp_server \
  --cov-report=xml \
  --cov-report=term \
  --junitxml=test-results.xml \
  --maxfail=1 \
  -v
```

## Watch Mode

For continuous testing during development:

```bash
# Install pytest-watch
pip install pytest-watch

# Run in watch mode
ptw

# Watch mode with options
ptw -- -v --maxfail=1
```

## Configuration

### Pytest Configuration (pytest.ini)

The project includes a comprehensive `pytest.ini` configuration:

- **Test Discovery**: Automatically finds `test_*.py` files
- **Markers**: Custom markers for organizing tests
- **Coverage**: Configured for the `src/mcp_server` package
- **Asyncio**: Auto mode for async test support
- **Warnings**: Error on warnings (except deprecated)
- **Minimum Python**: 3.10

### Environment Variables

```bash
# Use different config file
pytest -c custom_pytest.ini

# Override config options
pytest -o markers="custom: custom marker description"

# Ensure module is importable
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
pytest
```

## Writing Tests

### Test Structure

Tests follow the AAA pattern:
- **Arrange**: Set up test data and preconditions
- **Act**: Execute the code being tested
- **Assert**: Verify the results

### Using Fixtures

Shared fixtures are available in:
- `tests/conftest.py` - Project-wide fixtures
- `tests/fixtures/context.py` - Context-related fixtures
- `tests/fixtures/weather.py` - Weather-related fixtures

### Example Test

```python
import pytest
from mcp_server.models import ItineraryPreferences

@pytest.mark.unit
def test_valid_preferences():
    """Test creating valid itinerary preferences."""
    prefs = ItineraryPreferences(
        destination="Paris",
        start_date="2024-06-01",
        end_date="2024-06-07"
    )
    assert prefs.destination == "Paris"
    assert prefs.days == 7
```

## Best Practices

### Test Organization

1. **Unit Tests**: Test individual components in isolation
   - Mock external dependencies
   - Fast execution
   - High coverage of edge cases

2. **Integration Tests**: Test component interactions
   - Use real dependencies when possible
   - Test realistic scenarios
   - Verify end-to-end workflows

### Tips for Effective Testing

1. **Fast Feedback**: Start with `pytest tests/unit/ -x` for quick failures
2. **Debugging**: Use `pytest --pdb -x` to debug first failure immediately
3. **Coverage**: Use `pytest --cov=src --cov-report=html` for visual coverage analysis
4. **CI**: Use `pytest --maxfail=1 -v` to fail fast in continuous integration
5. **Development**: Use `ptw` (pytest-watch) for continuous testing during coding
6. **Isolation**: Keep unit tests isolated and fast
7. **Realistic**: Make integration tests reflect real-world usage
8. **Fixtures**: Reuse test fixtures to reduce duplication
9. **Markers**: Use markers to organize and filter tests effectively
10. **Documentation**: Add docstrings to explain what each test validates

## Useful Command Combinations

```bash
# Fast unit tests with coverage
pytest tests/unit/ --cov=src/mcp_server --cov-report=term -v

# Integration tests with detailed output
pytest tests/integration/ -vv -s

# All tests, stop on first failure, show coverage
pytest --cov=src/mcp_server -x -v

# Parallel execution with coverage (faster)
pytest -n auto --cov=src/mcp_server --cov-report=html

# Debug specific test with full context
pytest tests/unit/test_models.py::TestItineraryPreferences::test_valid_preferences -vv -s --pdb

# Pre-commit: fast unit tests with coverage
pytest tests/unit/ --cov=src/mcp_server --cov-report=term-missing -x

# CI-ready: comprehensive test with reports
pytest --cov=src/mcp_server --cov-report=xml --junitxml=results.xml -v --maxfail=1
```

## Troubleshooting

### Common Issues

**Import Errors**
```bash
# Ensure src is in PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
pytest
```

**Async Tests Not Running**
- Ensure `pytest-asyncio` is installed
- Check `asyncio_mode = auto` in `pytest.ini`

**Coverage Not Working**
- Install `pytest-cov`: `pip install pytest-cov`
- Verify source path: `--cov=src/mcp_server`

**Tests Running Slowly**
- Run unit tests only: `pytest tests/unit/`
- Use parallel execution: `pytest -n auto`
- Profile slow tests: `pytest --durations=10`

## Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [Pytest-asyncio Documentation](https://pytest-asyncio.readthedocs.io/)
- [Testing Best Practices](https://docs.pytest.org/en/latest/goodpractices.html)

## Test Statistics

Current test suite statistics:
- **Total Tests**: 54
- **Unit Tests**: 39 (5 test files)
- **Integration Tests**: 15 (2 test files)
- **Fixture Modules**: 3 modules
- **Test Markers**: 4 custom markers

## Continuous Integration

For CI/CD pipelines, use this configuration:

```yaml
# Example GitHub Actions configuration
- name: Run Tests
  run: |
    pytest \
      --cov=src/mcp_server \
      --cov-report=xml \
      --cov-report=term \
      --junitxml=test-results.xml \
      --maxfail=1 \
      -v
```

This will:
- Run all tests with verbose output
- Generate coverage reports (XML for CI integration)
- Create JUnit XML for test result reporting
- Fail fast on first error
- Display results in CI logs

