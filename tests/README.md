# Tests

## Running Tests

Install pytest first:
```bash
pip install pytest
```

Run all tests:
```bash
pytest
```

Run specific test file:
```bash
pytest tests/test_scraper_controls.py
```

Run with verbose output:
```bash
pytest -v
```

## Test Structure

- `test_scraper_controls.py` - Tests for start/stop functionality
  - State management (start/stop scraper)
  - Telegram command handling
  - Movie list display
  - Main loop behavior

## TDD Process

Tests follow Test-Driven Development:
1. Write failing test (RED)
2. Implement minimal code to pass (GREEN)
3. Refactor while keeping tests passing (REFACTOR)
