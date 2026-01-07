# Movie Show Web Scraper - Refactored

A modular web scraper that monitors cinema listings and sends Telegram notifications for new movies.

## Project Structure

```
movieshow-webscraper/
├── src/
│   ├── __init__.py
│   ├── core/                      # Core application components
│   │   ├── __init__.py
│   │   ├── error_handler.py       # Error handling and recovery
│   │   └── movie_scraper.py       # Web scraping logic
│   ├── services/                  # External services integration
│   │   ├── __init__.py
│   │   └── telegram_service.py    # Telegram notifications
│   └── utils/                     # Utility modules
│       ├── __init__.py
│       └── movies_manager.py      # Movies storage management
├── main.py                        # Application entry point
├── movieScraper.py               # Legacy entry point (deprecated)
├── config.py                      # Configuration (tokens, IDs)
├── run_scheduled.sh              # Scheduling script
├── currentmovies.txt             # Stored movie listings
└── requirements.txt              # Python dependencies
```

## Architecture

### Core Components

#### `ErrorHandler` (`src/core/error_handler.py`)
Manages application error states with intelligent notifications:
- Tracks first error occurrence
- Sends interval-based notifications for persistent errors
- Handles recovery with success notifications
- Configurable notification intervals

**Key Features:**
- Non-intrusive error handling with interval-based notifications
- Tracks time spent in error state
- Automatic recovery detection

#### `MovieScraper` (`src/core/movie_scraper.py`)
Web scraper using Selenium for dynamic content:
- Configurable Chrome WebDriver with headless mode
- Waits for elements to load dynamically
- Extracts movie titles using BeautifulSoup
- Context manager support for automatic resource cleanup

**Key Features:**
- Headless browser automation
- Dynamic content waiting
- Clean resource management

### Services

#### `TelegramService` (`src/services/telegram_service.py`)
Telegram bot integration for notifications:
- Send messages to specified chat
- Check API availability
- Error handling for network failures

**Key Features:**
- Simple, clean API for sending messages
- Connection validation

### Utilities

#### `MoviesManager` (`src/utils/movies_manager.py`)
Persistent storage and comparison of movie listings:
- Initialize and manage movies file
- Retrieve stored movie lists
- Save new movie lists
- Find newly added movies

**Key Features:**
- File-based persistence
- Automatic new movie detection
- Clean separation of concerns

## Usage

### Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Run the scraper
python main.py
```

### Configuration

Edit `config.py` with your Telegram credentials:

```python
telegram_token = "YOUR_BOT_TOKEN"
chat_id = "YOUR_CHAT_ID"
```

### Scheduled Execution

Run the scraper on a schedule using the provided shell script:

```bash
./run_scheduled.sh
```

The script runs the scraper between 7:30 AM and 11:00 PM daily.

## Development

### Adding New Services

Create a new service in `src/services/`:

```python
# src/services/new_service.py
class NewService:
    def __init__(self, config):
        self.config = config
    
    def send_notification(self, message: str) -> bool:
        # Implementation
        pass
```

### Extending Error Handling

The `ErrorHandler` can be extended for custom behavior:

```python
from src.core.error_handler import ErrorHandler

handler = ErrorHandler(
    notification_callback=custom_notify_func,
    notification_interval=600  # Custom interval
)
```

### Adding New Scrapers

Create additional scrapers by extending the pattern in `MovieScraper`:

```python
from src.core.movie_scraper import MovieScraper

scraper = MovieScraper(
    target_url="https://example.com",
    headless=True
)
movies = scraper.scrape_movies()
```

## Benefits of Refactoring

1. **Modularity**: Each component has a single responsibility
2. **Reusability**: Services and utilities can be used independently
3. **Testability**: Smaller, focused modules are easier to test
4. **Maintainability**: Clear separation of concerns
5. **Scalability**: Easy to add new services or features
6. **Error Handling**: Centralized, sophisticated error management with notifications

## Error Handling Strategy

The application uses a three-tier error handling approach:

1. **Scraping Errors**: Caught in `_scrape_and_check()` and reported to `ErrorHandler`
2. **Error State Management**: `ErrorHandler` tracks persistent errors and notifies at intervals
3. **Graceful Recovery**: When scraping succeeds after errors, recovery notification is sent

## Requirements

See `requirements.txt` for full dependencies:
- `selenium>=4.0.0` - Web browser automation
- `requests>=2.20.0` - HTTP requests
- `beautifulsoup4>=4.9.0` - HTML parsing

## Notes

- The legacy `movieScraper.py` is kept for backward compatibility but shouldn't be used directly
- Use `main.py` as the entry point for all operations
- The `currentmovies.txt` file is automatically created on first run
