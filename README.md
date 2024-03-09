# Software-ML-Assignment
This is a coding assignment.

In my first python file web_scraping_part1.py, I imported the necessary libraries:
re: Regular expression module for pattern matching.
pandas (aliased as pd): A powerful data manipulation library.
BeautifulSoup: A library for pulling data out of HTML and XML files.
requests: A library for making HTTP requests.

In the class of my first python file, I have three main methods:

__init__: Initializes the object with a given URL and initializes lists to store scraped data.
scrape_data: Scrapes data from the website using BeautifulSoup and appends it to the corresponding lists containing country, capital, population and area.
create_dataframe: I created a pandas DataFrame from the collected data.
Subsequently, I instantiate the CountryDataScraper class with a specific URL, scrape data, create a DataFrame, and save it as a CSV file.

In summary, this code is a web scraper designed to extract information about countries from a specified website and organize the data into a structured format using pandas.

In my second python file web_scraping_part2.py, I imported the necessary libraries:
BeautifulSoup: A library for pulling data out of HTML and XML files.
requests: A library for making HTTP requests.
pandas (aliased as pd): A powerful data manipulation library.

This class has three main methods:

__init__: Initializes the object with a base URL and a header for the data.
scrape_page: Scrapes data from a specified page, constructs the data in a tabular form, and appends it to the data list.
create_dataframe: Creates a pandas DataFrame from the collected data.
save_to_csv: Saves the DataFrame to a CSV file.

This example demonstrates how to use the TeamDataScraper class. It sets up the scraper with a base URL and a header, then iterates over four pages, scraping team data and finally saving it to a CSV file.

In summary, this code is a web scraper designed to extract hockey team statistics from a website, organize the data into a pandas DataFrame, and save it to a CSV file. The specific website being scraped is "https://www.scrapethissite.com/pages/forms/" as indicated by the base_url.

In my third python file web_scraping_and_mongo_upload.py, This code defines an Airflow Directed Acyclic Graph (DAG) for web scraping data from two different websites and uploading the scraped data to MongoDB. Let's break down the key components and their meaning:

Classes:
BaseScraper:

An abstract class providing a common structure for web scrapers.
Contains methods for initializing, scraping a page, extracting data, creating a DataFrame, and saving to a CSV file.
CountryDataScraper (inherits from BaseScraper):

Implements the extract_data method specific to scraping country data.
Scrapes information such as country name, capital, population, and area.
TeamDataScraper (inherits from BaseScraper):

Implements the extract_data method specific to scraping team data.
Scrapes information about hockey teams.
MongoDB Upload Function:
upload_to_mongodb:
A function to upload data from a CSV file to a MongoDB collection.
Uses the MongoHook from the Airflow MongoDB provider.
Airflow DAG:
DAG Configuration:

The DAG is named "web_scraping_and_mongo_upload_dag."
It has default arguments for the owner, start date, retries, and retry delay.
Scheduled to run weekly on Sunday at 12 AM.
Scraping and MongoDB Upload Tasks:

task_scrape_website_1:

PythonOperator for scraping country data from the first page.
Calls country_scraper.scrape_page with the argument 1.
task_scrape_website_2:

PythonOperator for scraping team data from four pages.
Calls team_scraper.scrape_page with the argument 4.
upload_country_details_to_mongodb:

PythonOperator for uploading country data to MongoDB.
Calls upload_to_mongodb with specific arguments.
upload_team_details_to_mongodb:

PythonOperator for uploading team data to MongoDB.
Calls upload_to_mongodb with specific arguments.
Task Dependencies:

task_scrape_website_1 is set to run before upload_country_details_to_mongodb.
task_scrape_website_2 is set to run before upload_team_details_to_mongodb.
Example Usage:
Country Data Scraping:

Scrapes country data from the URL "https://www.scrapethissite.com/pages/simple/".
Extracted data is saved to a CSV file at "C:/Users/masro/Downloads/country_details.csv."
Team Data Scraping:

Scrapes team data from the URL "https://www.scrapethissite.com/pages/forms/".
Extracted data is saved to a CSV file at "C:/Users/masro/Downloads/team_details.csv."
MongoDB Upload:

Uploads country details to the MongoDB collection named 'country_details_collection.'
Uploads team details to the MongoDB collection named 'team_details_collection.'
Task Dependencies:

Tasks are set up in a way that scraping tasks run first, and MongoDB upload tasks run after the respective scraping tasks are completed.
In summary, this Airflow DAG automates the process of web scraping country and team data every Sunday at 12am, saving it to CSV files, and uploading the data to MongoDB collections using PythonOperators and the specified dependencies.

For the case of my fourth python file selenium_web_jobs_extraction.py, 
This Python script uses the Selenium library to automate web scraping from the Bikroy website, specifically targeting job listings. After retrieving the necessary information, it translates the job titles from Bengali to English using the Google Translate API (provided by the googletrans library). Finally, it processes the translated job titles, removes unwanted characters, and saves the results to a CSV file.

Let's break down the code:

Selenium Setup:

python
Copy code
# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

# Create a Chrome webdriver object
driver = webdriver.Chrome()

# Navigate to the Bikroy website
driver.get("https://bikroy.com/")
Navigating to the "Jobs" Section:

python
Copy code
# Attempt to find the "Jobs" link using a more robust XPath
jobs_link = driver.find_element(By.XPATH, "//a[contains(@href,'jobs')]")
jobs_link.click()
Clicking on a Specific Job Category ("Chef" in this case):

python
Copy code
# Using WebDriverWait to ensure that the "Chef" link is clickable
chef_link = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'chef')]"))
)
chef_link.click()
Retrieving the Current URL and Making an HTTP Request:

python
Copy code
current_url = driver.current_url
response_url = requests.get(current_url)
html_content = response_url.text
Parsing HTML Using BeautifulSoup:

python
Copy code
# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')
Translating and Processing Job Titles:

python
Copy code
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

    # Translate the job title to English and process the result
    # ... (code for translation and processing)

# Create a DataFrame with translated job titles
data = {
    'Translated Job Titles': translated_job_titles
}

df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv("C:/Users/masro/Downloads/cheffinalreverse.csv")
In summary, this script automates the process of navigating through the Bikroy website, extracting job titles, translating them from Bengali to English, and saving the results to a CSV file. The translated job titles are processed to remove unwanted characters and ensure better readability.

For the case of fifth file, upload to mongodb.py, This code defines an Airflow Directed Acyclic Graph (DAG) for web scraping job titles from a website (specifically Bikroy), translating them from Bengali to English, and then uploading the translated titles to both a CSV file and a MongoDB collection. The code is organized into classes to encapsulate tasks and facilitate code reuse.

Let's break down the key components:

Classes:
BaseTask:

An abstract class that serves as the base for CSV and MongoDB tasks.
Contains common methods for web scraping, translation, and browser management.
CSVTasks (inherits from BaseTask):

Implements CSV-specific functionality such as saving translated job titles to a CSV file.
MongoDBTasks (inherits from BaseTask):

Implements MongoDB-specific functionality such as uploading translated job titles to a MongoDB collection.
Common Methods (in BaseTask):
scrape_and_translate:

Common web scraping and translation code. Specific implementation is left to subclasses.
close_browser:

Closes the web browser.
parse_html:

Parses the HTML content of the web page and returns job title elements.
translate_title:

Translates a given job title from Bengali to English and performs additional processing.
DAG Configuration:
default_args:

Configuration for the DAG, including owner, start date, retries, etc.
dag:

DAG configuration, including the DAG name, default arguments, and the schedule interval.
Tasks:
CSV and MongoDB Tasks Initialization:

Initialize instances of CSVTasks and MongoDBTasks classes, passing the WebDriver and the website URL.
Task Definitions:

scrape_translate_task:

PythonOperator that executes the scrape_and_translate method of CSVTasks.
Responsible for web scraping and translation.
upload_csv_task:

PythonOperator that executes the save_to_csv method of CSVTasks.
Saves translated job titles to a CSV file.
upload_mongodb_task:

PythonOperator that executes the upload_to_mongodb method of MongoDBTasks.
Uploads translated job titles to a MongoDB collection.
Task Dependencies:
Tasks are set up with dependencies, indicating the order of execution:
scrape_translate_task is followed by upload_csv_task.
upload_csv_task is followed by upload_mongodb_task.
This DAG automates the process of web scraping job titles, translating them, and storing the results in both a CSV file and a MongoDB collection. It can be scheduled to run at a specific interval (e.g., the first day of each month).

So if there is a conflict in two dag files, then, the second dag is given more priority than first dag by setting the first priority paramenter of first dag into 1.





















