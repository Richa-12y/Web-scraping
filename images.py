from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time

path="C:/Users/DELL/Downloads/chromedriver-win64/chromedriver.exe"
s=Service(path)
driver=webdriver.Chrome(service=s)
driver.get("https://www.google.com")

time.sleep(2)

box=driver.find_element_by_xpath("/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/textarea[1]")
box.send_keys("House of Dragon")
box.send_keys(Keys.ENTER)

time.sleep(3)

driver.find_element_by_xpath("""//*[@id="kp-wp-tab-overview"]/div[5]/div/div/div/div/div/div[1]/div/div/a""").click()

time.sleep(2)
driver.save_screenshot("C:/Users/DELL/Downloads/dragone1.png")
