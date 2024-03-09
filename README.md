# Software-ML-Assignment
This is a coding assignment.

In my first python file web_scraping_part1,py, I imported the necessary libraries:
re: Regular expression module for pattern matching.
pandas (aliased as pd): A powerful data manipulation library.
BeautifulSoup: A library for pulling data out of HTML and XML files.
requests: A library for making HTTP requests.

In the class of my first python, I have three main methods:

__init__: Initializes the object with a given URL and initializes lists to store scraped data.
scrape_data: Scrapes data from the website using BeautifulSoup and appends it to the corresponding lists containing country, capital, population and area.
create_dataframe: I created a pandas DataFrame from the collected data.
Subsequently, I instantiate the CountryDataScraper class with a specific URL, scrape data, create a DataFrame, and save it as a CSV file.

In summary, this code is a web scraper designed to extract information about countries from a specified website and organize the data into a structured format using pandas.



