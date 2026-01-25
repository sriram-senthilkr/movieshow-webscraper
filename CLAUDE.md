# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Application

The main entry point is `movieScraper.py`. It runs an infinite loop that polls a movie listing website every 10 seconds.

```bash
python movieScraper.py
```

**Behavior:**
- Script starts in PAUSED state
- Sends Telegram notification: "Bot started! Use /start to begin scraping"
- Waits for commands via Telegram

## Telegram Commands

Control the bot via Telegram:

- `/start` - Start scraping. Bot begins polling the website every 10 seconds
- `/stop` - Stop scraping. Bot enters idle mode
- `/list` - Show all movies currently being tracked
- `/status` - Show current bot state (Running/Stopped)

## Setup

1. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Create `config.py` in the project root with Telegram credentials:
   ```python
   telegram_token = "YOUR_TELEGRAM_BOT_TOKEN"
   chat_id = "YOUR_CHAT_ID"
   ```

3. Ensure Chrome/Chromium and Chromedriver are installed. The script attempts OS detection (movieScraper.py:22-36) to select the appropriate chromedriver path.

## Architecture

**State Machine:**
- The bot uses a `scraper_state` dictionary with `is_running` flag
- Starts in PAUSED state by default
- Background thread listens for Telegram commands
- Main loop checks state before each scrape cycle

**Main Loop Flow:**
1. Check `scraper_state["is_running"]`
2. If RUNNING: `scrape_new_movies()` → `retrieve_current_movies()` → `check_for_changes()` → sleep 10 seconds
3. If PAUSED: Sleep 2 seconds, then check state again
4. Repeat indefinitely

**Error Handling:**
- The script uses an `error_state` dictionary (movieScraper.py:48-54) to track error persistence
- `handle_error()` sends an initial error notification, then re-notifies every 20 minutes (1200 seconds) while errors persist
- `handle_recovery()` sends a recovery notification when the system returns to normal operation
- Error notifications go to Telegram with time-in-error tracking

**State Persistence:**
- `currentmovies.txt` stores one movie title per line (UTF-8 encoded)
- The file is initialized (cleared) on every script start via `initialize_movies_file()`
- File is only updated when new movies are detected

## Key Dependencies

- **selenium** - Headless browser automation for scraping dynamic content
- **beautifulsoup4** - HTML parsing
- **requests** - HTTP calls to Telegram Bot API
- **config** (local module) - Holds telegram_token and chat_id
- **pytest** - Testing framework (for running tests)

## Testing

Run the test suite:
```bash
pytest
```

Run specific tests:
```bash
pytest tests/test_scraper_controls.py
```

Tests are located in `tests/test_scraper_controls.py` and follow TDD methodology.
