"""Movie storage and management utilities."""

from typing import List
import os


class MoviesManager:
    """Manages persistent storage of movie listings."""

    def __init__(self, filepath: str = "currentmovies.txt"):
        """
        Initialize the movies manager.

        Args:
            filepath: Path to the file storing current movies
        """
        self.filepath = filepath

    def initialize(self) -> None:
        """Initialize the movies file, creating it if it doesn't exist."""
        try:
            with open(self.filepath, "w", encoding="utf-8") as file:
                file.write("")
            print(f"Initialized {self.filepath}")
        except Exception as e:
            print(f"Error initializing {self.filepath}: {str(e)}")
            raise

    def get_current_movies(self) -> List[str]:
        """
        Retrieve the list of currently stored movies.

        Returns:
            List of movie titles
        """
        try:
            if not os.path.exists(self.filepath):
                return []
            with open(self.filepath, "r", encoding="utf-8") as file:
                movies = [movie.strip() for movie in file.readlines()]
            return movies
        except Exception as e:
            print(f"Error reading movies from {self.filepath}: {str(e)}")
            return []

    def save_movies(self, movies: List[str]) -> None:
        """
        Save movies to storage.

        Args:
            movies: List of movie titles to save
        """
        try:
            with open(self.filepath, "w", encoding="utf-8") as file:
                for movie in movies:
                    file.write(f"{movie}\n")
            print(f"Saved {len(movies)} movies to {self.filepath}")
        except Exception as e:
            print(f"Error saving movies to {self.filepath}: {str(e)}")
            raise

    def find_new_movies(
        self, previous_movies: List[str], current_movies: List[str]
    ) -> List[str]:
        """
        Find movies that are new compared to the previous list.

        Args:
            previous_movies: Previously stored movie list
            current_movies: Current movie list from scraper

        Returns:
            List of new movie titles
        """
        return [movie for movie in current_movies if movie not in previous_movies]
