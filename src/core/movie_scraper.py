"""Web scraping module for fetching movie information."""

from typing import List
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


class MovieScraper:
    """Scraper for fetching movies from the cinema website."""

    def __init__(self, target_url: str, headless: bool = True):
        """
        Initialize the movie scraper.

        Args:
            target_url: URL to scrape
            headless: Whether to run Chrome in headless mode
        """
        self.target_url = target_url
        self.driver = self._initialize_chrome_driver(headless)

    def _initialize_chrome_driver(self, headless: bool) -> webdriver.Chrome:
        """Initialize and configure Chrome WebDriver."""
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")

        return webdriver.Chrome(options=chrome_options)

    def scrape_movies(self, timeout: int = 10) -> List[str]:
        """
        Scrape movie titles from the website.

        Args:
            timeout: Timeout for waiting for elements to load

        Returns:
            List of movie titles

        Raises:
            Exception: If scraping fails
        """
        try:
            self.driver.get(self.target_url)

            # Wait for the movies container to be present
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '[dynamic="Moviesdetails"]')
                )
            )

            soup = BeautifulSoup(element.get_attribute("outerHTML"), "html.parser")
            movie_listings = soup.find_all("div", class_="movies")

            movies = []
            for movie in movie_listings:
                h2_element = movie.find("h2")
                if h2_element:
                    movies.append(h2_element.text)

            return movies
        except Exception as e:
            raise Exception(f"Failed to scrape movies: {str(e)}")

    def close(self) -> None:
        """Close the WebDriver."""
        if self.driver:
            self.driver.quit()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
