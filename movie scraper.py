# import requests
# from bs4 import BeautifulSoup
# # import smtplib

# def check_for_new_movies():
#     url = 'https://carnivalcinemas.sg/#/Movies'

#     # Send an HTTP GET request to the website
#     response = requests.get(url)
    

#     # Check if the request was successful (status code 200)
#     if response.status_code == 200:
#         print("response 200 success")  # dubugging
#         print(response.text)
#         soup = BeautifulSoup(response.text, 'html.parser')

#         # Extract movie listings from the webpage
#         movie_listings = soup.find_all('div', class_='movies')  # Adjust class name as needed
#         print(movie_listings)

#         # Compare with previously stored movie data (you can store it in a file or database)
#         # For simplicity, let's assume the previous_movies variable contains the old movie listings
#         previous_movies = []

#         # Check for new movies
#         new_movies = [movie for movie in movie_listings if movie not in previous_movies]

#         if new_movies:
#             # If new movies are found, send an email notification
#             # send_email_notification(new_movies)
#             print("new_movies updates")

# # Function to send an email notification
# # def send_email_notification(new_movies):
# #     # Email configuration
# #     smtp_server = 'smtp.example.com'
# #     smtp_port = 587
# #     sender_email = 'your_email@example.com'
# #     sender_password = 'your_email_password'
# #     recipient_email = 'recipient@example.com'

# #     # Compose the email message
# #     subject = 'New Movies Added!'
# #     message = '\n'.join([str(movie) for movie in new_movies])

# #     # Connect to the SMTP server
# #     server = smtplib.SMTP(smtp_server, smtp_port)
# #     server.starttls()
# #     server.login(sender_email, sender_password)

# #     # Send the email
# #     server.sendmail(sender_email, recipient_email, f'Subject: {subject}\n\n{message}')

# #     # Disconnect from the server
# #     server.quit()

# # Example usage
# check_for_new_movies()


from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

chrome_options = Options()
chrome_options.add_argument('--headless') 
chrome_options.add_argument('--disable-dev-shm-usage')

chrome_path = r'C:\Program Files (x86)\chromedriver.exe'
chrome_service = ChromeService(chrome_path)
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

url = 'https://carnivalcinemas.sg/#/Movies'

driver.get(url)

# Wait for the element with class 'movies' to be present
element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '[dynamic="Moviesdetails"]'))
)

soup = BeautifulSoup(element.get_attribute('outerHTML'), 'html.parser')
movie_listings = soup.find_all('div', class_='movies')

driver.quit()


for movie in movie_listings:
    h2_element = movie.find('h2')
    if h2_element:
        h2_content = h2_element.text
        print(h2_content)

