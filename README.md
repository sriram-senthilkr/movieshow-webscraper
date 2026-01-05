<!-- PROJECT LOGO -->
<br />
<div align="center">
    <img src="images/movies_icon.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Simple Movie Webscraper</h3>

  <p align="center">
    Lightweight scraper that detects new movies on Carnival Cinemas and notifies a Telegram bot.
  </p>
</div>

## Overview

- **What it does:** Loads the Carnival Cinemas movies page, extracts movie titles from the rendered DOM, compares them to a local `currentmovies.txt`, and notifies a Telegram chat when there are new titles.
- **Main script:** `movieScraper.py`
- **Persistence:** `currentmovies.txt` (one title per line)

## Files

- **`movieScraper.py`**: Main scraper loop (Selenium + BeautifulSoup), change detection, and Telegram notifier.
- **`currentmovies.txt`**: Stores the last known list of movies.
- **`config.py`**: Local configuration for Telegram credentials (create/edit this file).
- **`requirements.txt`**: Python dependencies.
- **`images/`**: Assets used in the README.

## Prerequisites

- Python 3.8+
- Google Chrome (or Chromium) browser installed
- Chromedriver that matches your Chrome version (or use a compatible driver)

On macOS you can install Chromedriver via Homebrew:

```bash
# cask (preferred for GUI apps)
brew install --cask chromedriver

# or (if available)
brew install chromedriver
```

Confirm the chromedriver binary is present (e.g., `/usr/local/bin/chromedriver` or `/opt/homebrew/bin/chromedriver`).

## Setup

1. Clone the repo and change directory:

```bash
git clone <your-repo-url>
cd movieshow-webscraper
```

2. Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Create or edit `config.py` in the project root (a template `config.py` is provided). Fill your bot token and chat id:

```py
# config.py
telegram_token = "YOUR_TELEGRAM_BOT_TOKEN"
chat_id = "YOUR_CHAT_ID"
```

4. Update the Chromedriver path in `movieScraper.py` if necessary. By default the script contains a Windows path:

```py
chrome_path = r'C:\\Program Files (x86)\\chromedriver.exe'
```

Change it to your macOS path or put `chromedriver` on your `PATH` and update the code to use the correct location, e.g.:

```py
chrome_path = '/opt/homebrew/bin/chromedriver'
```

Alternatively you can modify `movieScraper.py` to use `webdriver-manager` (not installed by default) or mount the driver on PATH.

## Running the scraper

Run the script from the project root (with your virtualenv active):

```bash
python movieScraper.py
```

The script runs an infinite loop and polls the site every 10 seconds by default. To change the interval edit the `time.sleep(10)` line in `movieScraper.py`.

## How configuration works

- `config.py` contains `telegram_token` and `chat_id`. The script uses these to call the Telegram Bot API and post messages.
- `currentmovies.txt` is read on every scrape and overwritten when new movies are detected.

## Troubleshooting

- Selenium / Chromedriver errors:
  - Ensure Chromedriver version matches Chrome version.
  - Ensure the binary is executable and accessible (check `which chromedriver`).
  - If running headless on macOS, try removing the `--headless` flag to see browser output.

- Telegram notifications not working:
  - Confirm `telegram_token` and `chat_id` are correct. Test with a simple `curl` to the Bot API:

```bash
curl "https://api.telegram.org/bot${TOKEN}/sendMessage" -d chat_id=${CHAT_ID} -d text="test"
```

- File permission errors writing `currentmovies.txt`:
  - Ensure the script has write permission in the working directory.

## Suggested improvements

- Move configuration into environment variables or a `.env` file (avoid committing secrets).
- Add CLI flags to set chromedriver path, headless mode, and polling interval.
- Use `webdriver-manager` to avoid manual Chromedriver management.
- Add logging (Python `logging`) and rotate logs.
- Make the site-specific selectors configurable so the scraper can be reused for other sites.

## Running as a background job (example)

Simple `tmux` or `screen` session works. To run via `cron` (example, every 5 minutes):

```cron
# m h  dom mon dow command
*/5 * * * * /path/to/.venv/bin/python /path/to/movieshow-webscraper/movieScraper.py >> /path/to/movieshow-webscraper/scraper.log 2>&1
```

## Requirements

Install with

```bash
pip install -r requirements.txt
```