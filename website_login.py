from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configure Chrome options to connect to the existing Chrome instance
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

# Set up ChromeDriver service
try:
    driver_service = Service(ChromeDriverManager().install())
except Exception as e:
    print(f"Error setting up ChromeDriver service: {e}")
    exit()

# Initialize the ChromeDriver
try:
    driver = webdriver.Chrome(service=driver_service, options=chrome_options)
except OSError as e:
    print(f"Error initializing ChromeDriver: {e}")
    exit()

# Open the website
try:
    driver.get('https://sitagrimobile.financeagri.com')
except Exception as e:
    print(f"Error opening website: {e}")
    driver.quit()
    exit()

# Wait for the page to load (adjust the time as necessary)
time.sleep(5)

# Locate the username and password fields, and submit button
username_field = driver.find_element(By.NAME, "login")  # Adjust the ID as necessary
password_field = driver.find_element(By.NAME, "password")  # Adjust the ID as necessary
submit_button = driver.find_element(By.NAME, "signIn")  # Adjust the ID as necessary

# Input the login credentials (replace 'your_username' and 'your_password' with the actual credentials)
username_field.send_keys('danouer')
password_field.send_keys('Qm6k3uPe=o')

# Submit the form
submit_button.click()

# Wait for some time to ensure the login is processed (adjust the time as necessary)
time.sleep(5)

