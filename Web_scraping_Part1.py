import re
import pandas as pd
from bs4 import BeautifulSoup
import requests
class CountryDataScraper:
    def __init__(self, url):
        self.url = url
        self.country_names = []
        self.capitals = []
        self.populations = []
        self.areas = []

    def scrape_data(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')

        for row in soup.select('div.col-md-4.country'):
            country_name_elem = row.find('h3', class_='country-name')
            country_name = country_name_elem.text.strip() if country_name_elem else 'N/A'
            self.country_names.append(country_name)

            country_info_elem = row.find('div', class_='country-info')

            capital_elem = country_info_elem.find('strong', text=re.compile(r'Capital'))
            population_elem = country_info_elem.find('strong', text=re.compile(r'Population'))
            area_elem = country_info_elem.find('strong', text=re.compile(r'Area (km<sup>2</sup>)'))

            capital_span = capital_elem.find_next('span', class_='country-capital') if capital_elem else None
            population_span = population_elem.find_next('span', class_='country-population') if population_elem else None
            area_span = area_elem.find_next('span', class_='country-area') if area_elem else None

            capital = capital_span.text.strip() if capital_span else 'N/A'
            population = population_span.text.strip() if population_span else 'N/A'
            area = str(area_span.text.strip()) if area_span else 'N/A'

            self.capitals.append(capital)
            self.populations.append(population)
            self.areas.append(area_elem)

    def create_dataframe(self):
        data = {
            'Country': self.country_names,
            'Capital': self.capitals,
            'Population': self.populations,
            'Area': self.areas
        }
        return pd.DataFrame(data)

# Example usage
url = "https://www.scrapethissite.com/pages/simple/"
country_scraper = CountryDataScraper(url)
country_scraper.scrape_data()
df = country_scraper.create_dataframe()
df.to_csv("C:/Users/masro/Downloads/country_details.csv")





