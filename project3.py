import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Function to download an image with retries and timeouts
def download_image_with_retry(img_url, img_filename):
    retries = 3
    while retries > 0:
        try:
            img_data = requests.get(img_url, timeout=10).content
            with open(img_filename, 'wb') as img_file:
                img_file.write(img_data)
            return True
        except requests.exceptions.Timeout:
            print(f"Timeout while downloading {img_filename}. Retrying...")
            retries -= 1
        except Exception as e:
            print(f"Error while downloading {img_filename}: {str(e)}")
            return False
    return False

# Set up ChromeDriver with specific options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration

# Initialize the Chrome WebDriver with the executable_path
chrome_driver_path = 'C:/Users/DELL/Downloads/chromedriver-win64/chromedriver.exe'  # Specify your path
driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)
driver.maximize_window()

# Open the URL
url = 'https://www.wallpaperflare.com/search?wallpaper=ANIME'
driver.get(url)

# Create a folder for images
folder_name = 'animeimg'
os.makedirs(folder_name, exist_ok=True)

# Prompt the user for the number of pages to scrape
total_pages = int(input("Enter the number of pages to scrape: "))

# Scrape data from the specified number of pages
current_page = 1

while current_page <= total_pages:
    print(f"Scraping data from page {current_page}...")

    # Scroll down to load more images (you may need to adjust the number of scrolls)
    for _ in range(5):
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(2)

    # Parse the page content with Beautiful Soup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find all the image elements with the 'class' attribute containing 'lazy loaded'
    image_elements = soup.find_all('img', class_='lazy loaded')

    for i, img_element in enumerate(image_elements):
        try:
            img_url = img_element['data-src']
            if img_url:
                img_filename = f'{folder_name}/image_{current_page}_{i}.jpg'
                success = download_image_with_retry(img_url, img_filename)
                if success:
                    print(f"Downloaded {img_filename}")
        except Exception as e:
            print(f"Error while processing image {i} on page {current_page}: {str(e)}")

    # Go to the next page
    try:
        next_page_link = driver.find_element(By.PARTIAL_LINK_TEXT, 'Next Page')
        driver.get(next_page_link.get_attribute('href'))

        time.sleep(5)
        current_page += 1
    except NoSuchElementException:
        print("No next page found. Exiting the loop")

# Quit the WebDriver
driver.quit()

print("Scraping completed.")
