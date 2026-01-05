import time
import requests
import config
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

### chrome driver set-up
chrome_options = Options()
chrome_options.add_argument('--headless') 
chrome_options.add_argument('--disable-dev-shm-usage')

chrome_path = r'C:\Program Files (x86)\chromedriver.exe'
chrome_service = ChromeService(chrome_path)
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

murl = 'https://carnivalcinemas.sg/#/Movies'

### telegram bot set-up
url = f"https://api.telegram.org/bot{config.telegram_token}"

## variables
current_movies = []
new_movies = []

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
    except Exception as e:
        send_telegram_notification(f"An error has occured while scraping: {str(e)}")

def send_telegram_notification(message):
    params = {"chat_id": config.chat_id, "text": message}
    r = requests.get(url + "/sendMessage", params=params)

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




while True:
    try:
        scrape_new_movies(new_movies)
        current_movies = retrieve_current_movies()

        check_for_changes(current_movies, new_movies)
        new_movies = []

        # for url in urls_to_check:
        #     check_url(url)
    
        time.sleep(10)

    except Exception as e:
        send_telegram_notification(f"An error has occured: {str(e)}")
        driver.quit()
        break
