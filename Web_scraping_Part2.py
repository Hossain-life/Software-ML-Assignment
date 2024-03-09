from bs4 import BeautifulSoup
import requests
import pandas as pd
# Function to scrape data from a given page
class TeamDataScraper:
    def __init__(self, base_url, header):
        self.base_url = base_url
        self.header = header
        self.data = [self.header]

    def scrape_page(self, page):
        url = f"{self.base_url}?page={page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        for row in soup.find_all('tr', class_='team'):
            row_data = [td.text.strip() for td in row.find_all('td')]
            self.data.append(row_data)

    def create_dataframe(self):
        return pd.DataFrame(self.data[1:], columns=self.data[0])

    def save_to_csv(self, file_path):
        df = self.create_dataframe()
        df.to_csv(file_path, index=False)

# Example usage
base_url = 'https://www.scrapethissite.com/pages/forms/'
header = ['Team Name', 'Year', 'Wins', 'Losses', 'OT Losses', 'Win %', 'Goals For (GF)', 'Goals Against (GA)', '+ / -']

page_scraper = TeamDataScraper(base_url, header)

# Scraping data from the first to the fourth page
for page in range(1, 5):
    page_scraper.scrape_page(page)

# Save the DataFrame to CSV

page_scraper.save_to_csv("C:/Users/masro/Downloads/team_details.csv")





