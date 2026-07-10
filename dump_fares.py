import sys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

sys.path.insert(0, ".")
from scrapers.uber_scraper import UberScraper
from scrapers.rapido_scraper import RapidoScraper
from scrapers.ola_scraper import OlaScraper

def dump_html(scraper_cls, name):
    s = scraper_cls(headless=True)
    try:
        s.get_fare("Hawa Mahal, Jaipur, Rajasthan", "Jaipur International Airport, Sanganer")
    except Exception as e:
        pass
    with open(f"{name}_results.html", "w", encoding="utf-8") as f:
        f.write(s.driver.page_source)
    s.quit_driver()

if __name__ == "__main__":
    dump_html(UberScraper, "uber")
    dump_html(RapidoScraper, "rapido")
    dump_html(OlaScraper, "ola")
