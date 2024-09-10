from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.chrome.options import Options
from seleniumrequests import Chrome
import json
import requests
import re

def find_events_for_private_page():

    options = Options()
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")

    # Path to chromedriver in the same folder as the script
    driver_path = 'chromedriver'  # For macOS/Linux 
    # driver_path = 'chromedriver.exe'  # For Windows

    # Create a Service object
    service = Service(driver_path)

    # Initialize the WebDriver (Chrome in this case)
    driver = Chrome(options=options, service=service)

    # Facebook credentials
    email = "email"
    password = "password"

    # URL of the Facebook page you want to access
    facebook_page_url = "https://www.facebook.com/magnumsauna/upcoming_hosted_events"

    # Go to Facebook login page
    driver.get("https://www.facebook.com/login")

    # Allow time for the page to load
    time.sleep(3)

    # Find the email input and enter your email
    email_input = driver.find_element(By.ID, "email")
    email_input.send_keys(email)

    # Find the password input and enter your password
    password_input = driver.find_element(By.ID, "pass")
    password_input.send_keys(password)

    # Press Enter to log in
    password_input.send_keys(Keys.RETURN)

    # Wait for the login to complete
    time.sleep(5)

    # Navigate to the Facebook page
    driver.get(facebook_page_url)

    time.sleep(5)

    with open("page_source.html", "w", encoding='utf-8') as f:
        f.write(driver.page_source)
    
    with open("page_source.html", "r", encoding='utf-8') as f:
        content = f.read()
    
    return content


