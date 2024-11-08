import time
import json
import datetime
import logging
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ETFScraper:
    """A class to scrape ETF data from a website."""
    
    def __init__(self, headless=True, proxy=None):
        """Initialize the scraper with optional headless mode and proxy settings."""
        self.options = self._configure_browser_options(headless, proxy)
        self.driver = Chrome(options=self.options)
        self.base_url = 'https://farside.co.uk/?p=997'
        logging.info("Webdriver initialized.")

    def _configure_browser_options(self, headless, proxy):
        """Private method to configure browser options."""
        options = Options()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=2200,1300")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
        if proxy:
            options.add_argument(f'--proxy-server=socks5://{proxy}')
        return options

    def scrape(self):
        """Scrape the ETF data from the predefined URL."""
        try:
            self.driver.get(self.base_url)
            time.sleep(5)
            data = self._extract_data()
            logging.info("Data scraped successfully.")
            return data
        except Exception as e:
            logging.error(f"An error occurred: {e}")
        finally:
            self.driver.quit()
            logging.info("Webdriver closed.")

    def _extract_data(self):
        """Private method to extract data from the page."""
        yesterday_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%d %b %Y')
        rows = self.driver.find_elements(By.XPATH, '//*[@id="post-997"]/div[1]/div/figure/table/tbody/tr')
        
        formatted_data = []
        for i in range(2, len(rows) + 1):
            date_xpath = f'//*[@id="post-997"]/div[1]/div/figure/table/tbody/tr[{i}]/td[1]/span'
            date = self.driver.find_element(By.XPATH, date_xpath).text
            
            if date == yesterday_date:
                columns = ["IBIT", "FBTC", "BITB", "ARKB", "BTCO", "EZBC", "BRRR", "HODL", "BTCW", "GBTC", "DEFI", "Total"]
                etf_data = {col: self._get_cell_data(i, idx) for idx, col in enumerate(columns, start=2)}
                
                formatted_data.append({'date': date, 'data': etf_data})
        return formatted_data

    def _get_cell_data(self, row, col_index):
        """Retrieve text from a specific cell."""
        data_xpath = f'//*[@id="post-997"]/div[1]/div/figure/table/tbody/tr[{row}]/td[{col_index}]/div/span'
        return self.driver.find_element(By.XPATH, data_xpath).text

# Usage
#if __name__ == "__main__":
#    scraper = ETFScraper(headless=False)  # Set to False for debugging
#    data = scraper.scrape()
#    print(json.dumps(data, indent=4))  # Display the data as JSON
