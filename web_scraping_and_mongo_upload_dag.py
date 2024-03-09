import requests
import pandas as pd
from airflow.operators.python_operator import PythonOperator
from airflow.providers.mongo.hooks.mongo import MongoHook
from datetime import datetime, timedelta
from airflow import DAG
from bs4 import BeautifulSoup
import re

class BaseScraper:
    def __init__(self, base_url, header=None):
        self.base_url = base_url
        self.header = header
        self.data = [self.header] if header else []

    def scrape_page(self, page):
        url = f"{self.base_url}?page={page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.extract_data(soup)

    def extract_data(self, soup):
        raise NotImplementedError("Subclasses must implement the 'extract_data' method.")

    def create_dataframe(self):
        return pd.DataFrame(self.data[1:], columns=self.data[0])

    def save_to_csv(self, file_path):
        df = self.create_dataframe()
        df.to_csv(file_path, index=False)

class CountryDataScraper(BaseScraper):
    def extract_data(self, soup):
        for row in soup.select('div.col-md-4.country'):
            country_name_elem = row.find('h3', class_='country-name')
            country_name = country_name_elem.text.strip() if country_name_elem else 'N/A'
            self.data.append([country_name])

            country_info_elem = row.find('div', class_='country-info')
            capital_elem = country_info_elem.find('strong', text=re.compile(r'Capital'))
            population_elem = country_info_elem.find('strong', text=re.compile(r'Population'))
            area_elem = country_info_elem.find('strong', text=re.compile(r'Area \(km<sup>2</sup>\)'))

            capital_span = capital_elem.find_next('span', class_='country-capital') if capital_elem else None
            population_span = population_elem.find_next('span', class_='country-population') if population_elem else None
            area_span = area_elem.find_next('span', class_='country-area') if area_elem else None

            capital = capital_span.text.strip() if capital_span else 'N/A'
            population = population_span.text.strip() if population_span else 'N/A'
            area = str(area_span.text.strip()) if area_span else 'N/A'

            self.data[-1].extend([capital, population, area])

class TeamDataScraper(BaseScraper):
    def extract_data(self, soup):
        for row in soup.find_all('tr', class_='team'):
            row_data = [td.text.strip() for td in row.find_all('td')]
            self.data.append(row_data)

def upload_to_mongodb(collection_name, csv_file_path, **kwargs):
    # Connect to MongoDB
    hook = MongoHook(conn_id='mongo_conn_id') 
    # Replace with your MongoDB connection ID

    # Load CSV into DataFrame
    df = pd.read_csv(csv_file_path)

    # Convert DataFrame to JSON
    records = df.to_dict(orient='records')

    # Insert records into MongoDB collection
    hook.insert_many(collection_name, records)

# Define default_args
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Instantiate the DAG
dag = DAG(
    'web_scraping_and_mongo_upload_dag',
    default_args=default_args,
    description='A DAG for web scraping and uploading to MongoDB weekly on Sunday at 12 AM',
    schedule_interval='0 0 * * 0',  # Weekly on Sunday at 12 AM
    priority_weight=1,
)

# Instantiate the scraping classes
country_scraper = CountryDataScraper("https://www.scrapethissite.com/pages/simple/", header=['Country', 'Capital', 'Population', 'Area'])
team_scraper = TeamDataScraper("https://www.scrapethissite.com/pages/forms/")

# Define PythonOperators for scraping and MongoDB upload tasks
task_scrape_website_1 = PythonOperator(
    task_id='scrape_website_1',
    python_callable=country_scraper.scrape_page,
    op_args=[1],
    provide_context=True,
    dag=dag,
)

task_scrape_website_2 = PythonOperator(
    task_id='scrape_website_2',
    python_callable=team_scraper.scrape_page,
    op_args=[4],  # Specify the number of pages to scrape
    provide_context=True,
    dag=dag,
)

upload_country_details_to_mongodb = PythonOperator(
    task_id='upload_country_details_to_mongodb',
    python_callable=upload_to_mongodb,
    op_args=['country_details_collection', 'C:/Users/masro/Downloads/country_details.csv'],
    provide_context=True,
    dag=dag,
)

upload_team_details_to_mongodb = PythonOperator(
    task_id='upload_team_details_to_mongodb',
    python_callable=upload_to_mongodb,
    op_args=['team_details_collection', 'C:/Users/masro/Downloads/team_details.csv'],
    provide_context=True,
    dag=dag,
)

# Set task dependencies
task_scrape_website_1 >> upload_country_details_to_mongodb
task_scrape_website_2 >> upload_team_details_to_mongodb

