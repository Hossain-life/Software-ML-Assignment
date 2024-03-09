from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from pymongo import MongoClient
import pandas as pd
import requests
from bs4 import BeautifulSoup
from googletrans import Translator
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

class BaseTask:
    def __init__(self, driver, url):
        self.driver = driver
        self.url = url

    def scrape_and_translate(self):
        # Common web scraping and translation code here
        # ...

    def close_browser(self):
        self.driver.quit()

    def parse_html(self):
        response_url = requests.get(self.url)
        soup = BeautifulSoup(response_url.text, 'html.parser')
        return soup.find_all('h2', class_='heading--2eONR')

    def translate_title(self, job_title, translator):
        try:
            translation = translator.translate(job_title, src='bn', dest='en')
            english_title = translation.text
            english_title_no_digits = ''.join([char for char in english_title if not char.isdigit()])
            english_title_no_punctuation = english_title_no_digits.translate(str.maketrans('', '', string.punctuation))
            characters_to_remove = ['à', '।', '«']
            for char in characters_to_remove:
                english_title_no_punctuation = english_title_no_punctuation.replace(char, "")
            return english_title_no_punctuation.replace("Caisine", "Cuisine")
        except:
            return job_title

class CSVTasks(BaseTask):
    def save_to_csv(self, translated_job_titles):
        data = {'Translated Job Titles': translated_job_titles}
        df = pd.DataFrame(data)
        df.to_csv("C:/Users/masro/Downloads/chefversion.csv", index=False)

class MongoDBTasks(BaseTask):
    def upload_to_mongodb(self, translated_job_titles):
        df = pd.DataFrame({'Translated Job Titles': translated_job_titles})
        
        client = MongoClient("mongodb://your_mongodb_connection_string")
        db = client["chef_jobs"]
        collection = db["chefs"]
        
        records = df.to_dict(orient='records')
        collection.insert_many(records)
        
        client.close()

# DAG configuration
default_args = {
    'owner': 'your_name',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'upload_to_mongodb',
    default_args=default_args,
    schedule_interval='0 0 1 * *',  # Run at 12 AM on the first day of each month
)

# Driver initialization and website URL
driver = webdriver.Chrome()
url = "https://bikroy.com/"

# Instantiate CSV and MongoDB tasks
csv_task = CSVTasks(driver, url)
mongodb_task = MongoDBTasks(driver, url)

# Define tasks
scrape_translate_task = PythonOperator(
    task_id='scrape_and_translate_task',
    python_callable=csv_task.scrape_and_translate,  # Use CSV specific function
    dag=dag,
)

upload_csv_task = PythonOperator(
    task_id='upload_csv_task',
    python_callable=csv_task.save_to_csv,
    dag=dag,
)

upload_mongodb_task = PythonOperator(
    task_id='upload_to_mongodb_task',
    python_callable=mongodb_task.upload_to_mongodb,
    dag=dag,
)

# Set the task dependencies
scrape_translate_task >> upload_csv_task >> upload_mongodb_task

