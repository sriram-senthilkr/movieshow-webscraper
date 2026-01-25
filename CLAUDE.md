# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Application

The main entry point is `movieScraper.py`. It runs an infinite loop that polls a movie listing website every 10 seconds.

```bash
python movieScraper.py
```

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

**Main Loop Flow:**
1. `scrape_new_movies()` - Uses Selenium to fetch the Carnival Cinemas page, waits for `[dynamic="Moviesdetails"]` element, extracts movie titles from `<div class='movies'><h2>` elements
2. `retrieve_current_movies()` - Reads previously seen movies from `currentmovies.txt`
3. `check_for_changes()` - Compares new vs current, writes new list to file if changed, sends Telegram notification for new movies
4. Sleeps 10 seconds and repeats

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
