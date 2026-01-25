# Start/Stop Controls Design

**Date:** 2026-01-25
**Status:** Approved

## Overview

Add interactive control to the movie scraper bot with Telegram commands (`/start`, `/stop`, `/list`) and a simple CLI debug interface. The scraper will use a state machine approach with PAUSED and RUNNING states.

## Architecture

### State Machine

The bot uses a simple state variable to control scraping behavior:

```python
scraper_state = {
    "is_running": False,  # Start paused by default
    "command": None
}
```

**States:**
- **RUNNING** (`is_running=True`): Scraper polls the website every 10 seconds
- **PAUSED** (`is_running=False`): Scraper idles, checks every 2 seconds for state changes

### Main Loop Integration

The main loop checks state before each scrape cycle:

```python
def main_loop():
    while True:
        if scraper_state["is_running"]:
            scrape_new_movies(new_movies)
            current_movies = retrieve_current_movies()
            check_for_changes(current_movies, new_movies)
            new_movies = []
            time.sleep(10)
        else:
            # Paused - wait briefly before checking again
            time.sleep(2)
```

**Startup Behavior:**
- Script starts in PAUSED state
- Sends Telegram message: "Bot started. Use /start to begin scraping"
- Command listener starts immediately, ready to accept commands

## Telegram Commands

### Command Interface

A daemon thread runs `telegram_command_listener()` that polls for updates:

**Commands:**
- `/start` - Begins scraping. If already running, replies "Scraper is already running"
- `/stop` - Pauses scraping. If already paused, replies "Scraper is already stopped"
- `/list` - Shows all movies in `currentmovies.txt` formatted as a list
- `/status` - Shows current state, time since last scrape, error status

### Implementation

```python
def telegram_command_listener():
    last_update_id = 0
    while True:
        try:
            response = requests.get(f"{url}/getUpdates", params={"offset": last_update_id + 1})
            updates = response.json().get("result", [])

            for update in updates:
                message = update.get("message", {})
                text = message.get("text", "")
                chat_id = message.get("chat", {}).get("id")

                if text == "/start": start_scraper()
                elif text == "/stop": stop_scraper()
                elif text == "/list": show_current_list()

                last_update_id = update["update_id"]
        except Exception as e:
            print(f"Command listener error: {e}")

        time.sleep(2)
```

**Thread Safety:**
- Python's GIL provides basic thread safety for simple boolean state
- No complex locking needed

## CLI Debug Interface

Simple `input()` based interface for local debugging:

```python
if __name__ == "__main__":
    print("CLI debug mode. Type 'start', 'stop', 'list', 'exit'")
    command_thread = Thread(target=cli_input_loop, daemon=True)
    command_thread.start()
```

## State Persistence

No changes to existing persistence:
- `currentmovies.txt` still initialized (cleared) on script start
- Updated only when new movies are detected
- Existing `error_state` system continues unchanged

## Error Handling

**Existing error handling preserved:**
- Scraping errors tracked in `error_state` dictionary
- `handle_error()` and `handle_recovery()` continue as-is

**New error handling:**
- Command listener errors logged but don't crash the thread
- If command thread crashes, main scraper continues unaffected

## Edge Cases

- `/stop` while paused → Reply "Already stopped"
- `/start` while running → Reply "Already running"
- Empty movie list → `/list` replies "No movies currently tracked"
- Telegram API rate limits → Command listener has 2-second delay
- No internet connection → Both scraper and command listener handle gracefully

## Testing Strategy

1. **Start the bot** - Verify startup message and PAUSED state
2. **Test `/start`** - Confirm scraping begins
3. **Test `/stop`** - Confirm scraping pauses
4. **Test `/list`** - Verify movies display correctly
5. **Test edge cases** - Duplicate commands, empty lists
6. **Test CLI debug mode** - Verify local commands work
7. **Integration test** - Detect new movie, verify notification, stop/restart
