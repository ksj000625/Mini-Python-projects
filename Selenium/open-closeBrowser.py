from selenium import webdriver
import time

# webdriver.Chrome("/home/dell/Python projects/Selenium/chromedriver")
browser = webdriver.Chrome("/home/dell/Python projects/Selenium/chromedriver")
dir(browser)
browser.get("https://www.facebook.com")
time.sleep(10)
browser.close()