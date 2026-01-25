import time
import requests
import config
import os
import platform
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

### chrome driver set-up
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')

# Detect OS and use appropriate chromedriver
system = platform.system()
if system == 'Linux':
    # For Raspberry Pi and Linux systems
    service = ChromeService(executable_path='/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)
elif system == 'Darwin':
    # For macOS
    driver = webdriver.Chrome(options=chrome_options)
elif system == 'Windows':
    # For Windows
    driver = webdriver.Chrome(options=chrome_options)
else:
    # Fallback for unknown OS
    driver = webdriver.Chrome(options=chrome_options)

murl = 'https://carnivalcinemas.sg/#/Movies'

### telegram bot set-up
url = f"https://api.telegram.org/bot{config.telegram_token}"

## variables
current_movies = []
new_movies = []

# Error tracking
error_state = {
    "in_error": False,
    "error_message": None,
    "first_error_time": None,
    "last_notification_time": None,
    "notification_interval": 1200  # Notify every 5 minutes while in error state
}

# Scraper state for start/stop controls
scraper_state = {
    "is_running": False,  # Start paused by default
    "command": None
}

# Initialize currentmovies.txt on script start
def initialize_movies_file():
    try:
        with open('currentmovies.txt', 'w', encoding='utf-8') as file:
            file.write('')  # Create empty file or clear existing contents
        print("currentmovies.txt initialized")
    except Exception as e:
        send_telegram_notification(f"Error initializing currentmovies.txt: {str(e)}")
        print(f"Error initializing currentmovies.txt: {str(e)}")

def scrape_new_movies(new_movies):
    try:
    ### execution
        driver.get(murl)

        # Wait for the element with class 'movies' to be present
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[dynamic="Moviesdetails"]'))
        )

        soup = BeautifulSoup(element.get_attribute('outerHTML'), 'html.parser')
        movie_listings = soup.find_all('div', class_='movies')


        for movie in movie_listings:
            h2_element = movie.find('h2')
            if h2_element:
                h2_content = h2_element.text
                new_movies.append(h2_content)
        
        # If we were in error state and now succeeded, reset it
        handle_recovery()
        
    except Exception as e:
        handle_error(f"An error has occured while scraping: {str(e)}")

def send_telegram_notification(message):
    params = {"chat_id": config.chat_id, "text": message}
    r = requests.get(url + "/sendMessage", params=params)

def handle_error(error_message):
    """Handle errors gracefully with interval-based notifications"""
    now = datetime.now()
    
    if not error_state["in_error"]:
        # First time hitting this error
        error_state["in_error"] = True
        error_state["error_message"] = error_message
        error_state["first_error_time"] = now
        error_state["last_notification_time"] = now
        send_telegram_notification(f"❌ ERROR DETECTED:\n{error_message}\n\nWill notify you every 20 minutes if issue persists.")
        print(f"[ERROR] {error_message}")
    else:
        # Already in error state, check if we should notify again
        time_since_last_notification = (now - error_state["last_notification_time"]).total_seconds()
        
        if time_since_last_notification >= error_state["notification_interval"]:
            time_in_error = (now - error_state["first_error_time"]).total_seconds() / 60
            send_telegram_notification(f"⏱️ Still having issues (for {int(time_in_error)} minutes):\n{error_message}")
            error_state["last_notification_time"] = now
            print(f"[ERROR - {int(time_in_error)} min] {error_message}")

def handle_recovery():
    """Handle recovery from error state"""
    if error_state["in_error"]:
        time_in_error = (datetime.now() - error_state["first_error_time"]).total_seconds() / 60
        send_telegram_notification(f"✅ SERVICE RECOVERED!\nSystem is back to normal after {int(time_in_error)} minutes of errors.")
        print(f"[RECOVERED] Service back to normal after {int(time_in_error)} minutes")
        error_state["in_error"] = False
        error_state["error_message"] = None
        error_state["first_error_time"] = None
        error_state["last_notification_time"] = None

def retrieve_current_movies():
    try:
        with open('currentmovies.txt', 'r', encoding='utf-8') as file:
            movies_list = file.readlines()
            movies_list = [movie.strip() for movie in movies_list]
    except FileNotFoundError:
        movies_list = []
    return movies_list

def check_for_changes(current_movies, new_movies):
    changed_movies = [movie for movie in new_movies if movie not in current_movies]
    
    if changed_movies:
        with open('currentmovies.txt', 'w', encoding='utf-8') as file:
            for movie in new_movies:
                file.write(movie + '\n')
        message = "New movies detected:" + "\n" + "\n".join(changed_movies)
        send_telegram_notification(message)
        print(message)

def check_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            send_telegram_notification(f"{url} is available")
            print(f"{url} is available")
    except requests.exceptions.RequestException as e:
        send_telegram_notification(f"(Error: {e}) {url} is not available")
        print(f"(Error: {e}) {url} is not available")

# Start/Stop control functions
def start_scraper():
    """Start the scraper if not already running."""
    if not scraper_state["is_running"]:
        scraper_state["is_running"] = True
        send_telegram_notification("✅ Scraper started!")
        print("[START] Scraper started")
    else:
        send_telegram_notification("Scraper is already running")
        print("[START] Already running")

def stop_scraper():
    """Stop the scraper if not already stopped."""
    if scraper_state["is_running"]:
        scraper_state["is_running"] = False
        send_telegram_notification("⏸️ Scraper stopped!")
        print("[STOP] Scraper stopped")
    else:
        send_telegram_notification("Scraper is already stopped")
        print("[STOP] Already stopped")

def show_current_list():
    """Display the current list of movies being tracked."""
    movies = retrieve_current_movies()
    if movies:
        message = "📽️ Current movies:\n" + "\n".join(f"• {movie}" for movie in movies)
    else:
        message = "No movies currently tracked"
    send_telegram_notification(message)
    print(f"[LIST] Showing {len(movies)} movies")

def handle_telegram_command(update):
    """Handle an incoming Telegram command update."""
    message = update.get("message", {})
    text = message.get("text", "")

    if text == "/start":
        start_scraper()
    elif text == "/stop":
        stop_scraper()
    elif text == "/list":
        show_current_list()
    elif text == "/status":
        status = "Running" if scraper_state["is_running"] else "Stopped"
        send_telegram_notification(f"📊 Status: {status}")
        print(f"[STATUS] {status}")
    # Unknown commands are silently ignored

def telegram_command_listener():
    """Background thread to listen for Telegram commands."""
    last_update_id = 0
    while True:
        try:
            response = requests.get(f"{url}/getUpdates", params={"offset": last_update_id + 1}, timeout=5)
            if response.status_code == 200:
                updates = response.json().get("result", [])

                for update in updates:
                    handle_telegram_command(update)
                    last_update_id = update["update_id"]
        except Exception as e:
            print(f"[COMMAND LISTENER ERROR] {str(e)}")

        time.sleep(2)




# Initialize the movies file when script starts
initialize_movies_file()

# Start the command listener thread in the background
command_thread = threading.Thread(target=telegram_command_listener, daemon=True)
command_thread.start()
print("[INIT] Command listener thread started")

# Send startup notification
send_telegram_notification("🤖 Bot started! Use /start to begin scraping.")
print("[INIT] Bot started in PAUSED state. Waiting for /start command...")

while True:
    try:
        if scraper_state["is_running"]:
            # Running state: scrape as normal
            scrape_new_movies(new_movies)
            current_movies = retrieve_current_movies()
            check_for_changes(current_movies, new_movies)
            new_movies = []
            time.sleep(10)
        else:
            # Paused state: just wait briefly before checking again
            time.sleep(2)

    except Exception as e:
        handle_error(f"Unexpected error in main loop: {str(e)}")
        time.sleep(30)
