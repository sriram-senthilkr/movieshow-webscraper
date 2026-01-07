"""Main entry point for the movie scraper application."""

import time
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import config
from src.core.movie_scraper import MovieScraper
from src.core.error_handler import ErrorHandler
from src.services.telegram_service import TelegramService
from src.utils.movies_manager import MoviesManager


class MovieScraperApp:
    """Main application orchestrating movie scraping and notifications."""

    def __init__(
        self,
        scraper_url: str,
        config_token: str,
        config_chat_id: str,
        movies_file: str = "currentmovies.txt",
        sleep_interval: int = 10,
        error_sleep_interval: int = 30,
    ):
        """
        Initialize the movie scraper application.

        Args:
            scraper_url: URL to scrape for movies
            config_token: Telegram bot token
            config_chat_id: Telegram chat ID
            movies_file: Path to movies storage file
            sleep_interval: Seconds to sleep between scrapes
            error_sleep_interval: Seconds to sleep after an error
        """
        self.scraper_url = scraper_url
        self.movies_file = movies_file
        self.sleep_interval = sleep_interval
        self.error_sleep_interval = error_sleep_interval

        # Initialize services
        self.telegram = TelegramService(config_token, config_chat_id)
        self.error_handler = ErrorHandler(self.telegram.send_message)
        self.movies_manager = MoviesManager(movies_file)
        self.scraper = MovieScraper(scraper_url)

    def run(self) -> None:
        """Run the main application loop."""
        try:
            # Initialize movies file
            self.movies_manager.initialize()

            # Main loop
            while True:
                self._scrape_and_check()
                time.sleep(self.sleep_interval)

        except KeyboardInterrupt:
            print("\nShutting down gracefully...")
            self.shutdown()
        except Exception as e:
            self.error_handler.handle_error(f"Unexpected error in main loop: {str(e)}")
            self.shutdown()

    def _scrape_and_check(self) -> None:
        """Scrape movies and check for changes."""
        try:
            # Scrape new movies
            new_movies = self.scraper.scrape_movies()

            # Get previously stored movies
            current_movies = self.movies_manager.get_current_movies()

            # Find new movies
            changed_movies = self.movies_manager.find_new_movies(
                current_movies, new_movies
            )

            if changed_movies:
                # Save new movies
                self.movies_manager.save_movies(new_movies)

                # Notify user
                message = "New movies detected:\n" + "\n".join(changed_movies)
                self.telegram.send_message(message)
                print(message)

            # If we were in error state and now succeeded, recover
            self.error_handler.handle_recovery()

        except Exception as e:
            self.error_handler.handle_error(f"Error during scraping: {str(e)}")
            time.sleep(self.error_sleep_interval)

    def shutdown(self) -> None:
        """Clean up resources."""
        try:
            self.scraper.close()
            print("Scraper closed successfully")
        except Exception as e:
            print(f"Error closing scraper: {e}")


def main():
    """Entry point for the application."""
    app = MovieScraperApp(
        scraper_url="https://carnivalcinemas.sg/#/Movies",
        config_token=config.telegram_token,
        config_chat_id=config.chat_id,
    )
    app.run()


if __name__ == "__main__":
    main()
