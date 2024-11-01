from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from seleniumrequests import Chrome
import os

# Set up the WebDriver (make sure to replace 'path_to_your_driver' with the actual path to your WebDriver)
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

# Open the webpage
driver.get("https://gpt-4-vision-react-starter.vercel.app/")  # Replace with the actual URL

# Wait for the page to load
time.sleep(3)

# Locate the text input field and type your input
input_field = driver.find_element(By.XPATH, "//input[@placeholder='Enter a custom question or prompt']")
input_field.send_keys("give me the event name, the exact, factual date and start time of the pictured event in a json format. Year should be exact and double checked")  # Repl

# Locate the hidden file input and send the file path
file_input = driver.find_element(By.ID, "fileUpload")
absolute_image_path = os.path.abspath('small.jpg')
file_path = absolute_image_path  # Replace with the path to your image
file_input.send_keys(file_path)

# Click the "Analyze Image" button
analyze_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Analyze Image')]")
analyze_button.click()

# Wait for the result to appear
time.sleep(5)

# Locate the analysis result textarea and get its content
result_textarea = driver.find_element(By.XPATH, "//div[@class='mt-5']//textarea")
analysis_result = result_textarea.get_attribute("value")

# Print or use the analysis result as needed
print("Analysis Result:", analysis_result)

# Close the driver
driver.quit()