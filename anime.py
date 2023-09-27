import os
import time
import requests
from selenium import webdriver

# Set up ChromeDriver
driver = webdriver.Chrome(executable_path='C:/Users/DELL/Downloads/chromedriver-win64/chromedriver.exe')
driver.maximize_window()

# Open the URL
url = 'https://www.wallpaperflare.com/search?wallpaper=ANIME'
driver.get(url)

# Create a folder for images
folder_name = 'animeimg'
os.makedirs(folder_name, exist_ok=True)

# Scrape data from multiple pages
current_page = 1
total_pages = 20  # Increase to 20 pages

while current_page <= total_pages:
    print(f"Scraping data from page {current_page}...")

    # Find all the image elements with the 'class' attribute containing 'lazy loaded'
    image_elements = driver.find_elements_by_css_selector('img.lazy.loaded')

    for i, img_element in enumerate(image_elements):
        try:
            img_url = img_element.get_attribute('data-src')
            if img_url:
                retries = 3
                while retries > 0:
                    try:
                        img_data = requests.get(img_url, timeout=10).content
                        # Save the image
                        img_filename = f'{folder_name}/image_{current_page}_{i}.jpg'
                        with open(img_filename, 'wb') as img_file:
                            img_file.write(img_data)
                        break
                    except requests.exceptions.Timeout:
                        print(f"Timeout while downloading image {i} on page {current_page}. Retrying...")
                        retries -= 1
                    except Exception as e:
                        print(f"Error while downloading image {i} on page {current_page}: {str(e)}")
                        break
        except Exception as e:
            print(f"Error while processing image {i} on page {current_page}: {str(e)}")

    # Go to the next page
    try:
        next_page_link = driver.find_element_by_link_text('Next Page')
        driver.get(next_page_link.get_attribute('href'))

        time.sleep(5)
        current_page += 1

    except NoSuchElementException:
        print("No next page found. Exiting the loop")

driver.quit()
