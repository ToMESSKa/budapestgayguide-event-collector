from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from seleniumrequests import Chrome
import os
from selenium.common.exceptions import NoSuchElementException

def get_events_from_analizing_pictures(filename):
    # Set up the WebDriver (make sure to replace 'path_to_your_driver' with the actual path to your WebDriver)
    options = Options()
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")

    # Path to chromedriver in the same folder as the script
    driver_path = 'chromedriver'

    # Create a Service object
    service = Service(driver_path)

    # Initialize the WebDriver (Chrome in this case)
    driver = Chrome(options=options, service=service)

    # Open the webpage
    driver.get("https://gpt-4-vision-react-starter.vercel.app/")  # Replace with the actual URL

    # Wait for the page to load
    time.sleep(6)

    # Locate the text input field and type your input
    input_field = driver.find_element(By.XPATH, "//input[@placeholder='Enter a custom question or prompt']")
    input_field.send_keys("Do not include past events in the results. Please analyze the image I provided and return the result in a JSON object format with the following keys: event_name, time and date. If any of these keys do not have meaningful or relevant information based on the image content, skip the image. Here’s what I need for each key:event_name: Get the exact name of the event. If the picture contains words like 'horny',  'gang bang', 'fist', 'cum', please provide a censored version for the the name like *ang bang'date: this should be the date in the format YYYY.MM.DD, please make sure the year is correct and okay time: this should be the starting time in format HH:MM JSON Object Format: { 'event_name': 'event name','time': 'time','date': 'date'}")

    # Locate the hidden file input and send the file path
    file_input = driver.find_element(By.ID, "fileUpload")
    absolute_image_path = os.path.abspath(filename)
    file_path = absolute_image_path  # Replace with the path to your image
    file_input.send_keys(file_path)

    # Click the "Analyze Image" button
    try:
        analyze_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Analyze Image')]")
        analyze_button.click()
    except NoSuchElementException:
        print()


    # Wait for the result to appear
    time.sleep(10)

    # Locate the analysis result textarea and get its content
    try:
        result_textarea = driver.find_element(By.XPATH, "//div[@class='mt-5']//textarea")
        analysis_result = result_textarea.get_attribute("value")
        return analysis_result
    except NoSuchElementException:
        print()
