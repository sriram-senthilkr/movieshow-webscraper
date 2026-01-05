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

On Linux (Debian/Ubuntu) you can install Chrome + Chromedriver in a few ways:

- Option A — install Chromium and the packaged chromedriver (may be out-of-date on some distros):

```bash
sudo apt update
sudo apt install -y chromium-browser chromium-chromedriver
```

- Option B — install Google Chrome and download the matching Chromedriver manually:

1. Install Google Chrome (Debian/Ubuntu example):

```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb || sudo apt -f install -y
```

2. Find your Chrome version (`google-chrome --version`) and download the corresponding Chromedriver from https://chromedriver.chromium.org/downloads. Extract the binary and move it to `/usr/local/bin` or `/usr/bin`:

```bash
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver
```

You can verify the driver with `which chromedriver` or `/usr/local/bin/chromedriver --version`.

On macOS you can still use Homebrew:

```bash
# cask (preferred for GUI apps)
brew install --cask chromedriver

# or (if available)
brew install chromedriver
```

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

4. Chromedriver path and environment variable

The scraper now checks the `CHROMEDRIVER_PATH` environment variable (recommended) and falls back to `/usr/bin/chromedriver` by default. Set the env var if your chromedriver is installed in a non-standard location:

```bash
export CHROMEDRIVER_PATH=/usr/local/bin/chromedriver
# or, for example, /opt/homebrew/bin/chromedriver on macOS
```

No code change is required if `chromedriver` is on your `PATH` and installed to a standard location. If you prefer a hardcoded path, edit the `chrome_path` value in `movieScraper.py`.

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

### Optional: Automated Chromedriver install with `setup.sh`

If you'd like a helper to install a matching Chromedriver on Debian/Ubuntu, there's a `setup.sh` script included at the repo root. It will attempt to detect your Chrome/Chromium version, download the corresponding Chromedriver, move it to `/usr/local/bin`, and add a `CHROMEDRIVER_PATH` export to your `~/.profile`.

Run (as root or with `sudo`):

```bash
chmod +x setup.sh
sudo ./setup.sh
```

After the script finishes either open a new shell or run:

```bash
source ~/.profile
export CHROMEDRIVER_PATH=/usr/local/bin/chromedriver
```

Then run the scraper as usual:

```bash
/path/to/.venv/bin/python movieScraper.py
```

This `setup.sh` option is provided in addition to the manual install options above — you can keep using whichever method you prefer.

## Requirements

Install with

```bash
pip install -r requirements.txt
```