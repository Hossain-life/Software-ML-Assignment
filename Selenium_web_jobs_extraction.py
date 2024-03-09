from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import requests
from bs4 import BeautifulSoup
from googletrans import Translator
import string
import pandas as pd
# create webdriver object
driver = webdriver.Chrome()

# get the website
driver.get("https://bikroy.com/")

# sleep for some time
#sleep(3)

# Attempt to get the "Jobs" link using a more robust XPath (adjust as needed)
jobs_link = driver.find_element(By.XPATH, "//a[contains(@href,'jobs')]")  
jobs_link.click()

# wait for the new page to load (you can adjust the sleep duration or use WebDriverWait for better handling)
#sleep(4)

# get the current URL after clicking the "Jobs" link
#current_url = driver.current_url
#print("Current URL:", current_url)

# Clicking on a "Chef" link on the current page (replace with the actual locator for the Chef link)
try:
    chef_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'chef')]"))
    )
    chef_link.click()
    #print("Clicked on 'Chef' link")
except Exception as e:
    print("Error clicking on 'Chef' link:", str(e))

# wait for the new page to load (you can adjust the sleep duration or use WebDriverWait for better handling)
#sleep(10)
current_url = driver.current_url
#response_url = requests.get(current_url)
# Add additional steps here based on the new page's URL

# Close the browser window
driver.quit()
# Assuming response_url.text contains the HTML content
response_url = requests.get(current_url)
# Assuming response_url.text contains the HTML content
html_content = response_url.text

# Parse HTML using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find all instances of job titles
job_title_elements = soup.find_all('h2', class_='heading--2eONR')

# Initialize an empty list to store translated job titles
translated_job_titles = []

# Create a translator object
translator = Translator()

# Define a translation table to remove punctuation
translator_remove_punctuation = str.maketrans('', '', string.punctuation)

# Define characters to remove
characters_to_remove = ['à', '।', '«']

# Iterate through each job title element
for job_title_element in job_title_elements:
    # Extract job title
    job_title = job_title_element.text.strip()

    # Translate the job title to English
    try:
        translation = translator.translate(job_title, src='bn', dest='en')
        english_title = translation.text

        # Remove digits from the translated job title
        english_title_no_digits = ''.join([char for char in english_title if not char.isdigit()])

        # Remove punctuation from the translated job title
        english_title_no_punctuation = english_title_no_digits.translate(translator_remove_punctuation)

        # Remove specified characters from the translated job title
        for char in characters_to_remove:
            english_title_no_punctuation = english_title_no_punctuation.replace(char, "")
        
        english_title_corrected = english_title_no_punctuation.replace("Caisine", "Cuisine")

        # Check if the result is not empty or whitespace-only
        if english_title_corrected.strip():
            translated_job_titles.append(english_title_no_punctuation)
    except:
        # If translation fails, keep the original title
        translated_job_titles.append(job_title)

# Create a DataFrame with a single column for all translated job titles
data = {
    'Translated Job Titles': translated_job_titles
}

df = pd.DataFrame(data)
df.to_csv("C:/Users/masro/Downloads/cheffinalreverse.csv")





