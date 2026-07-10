import sys
import time
sys.path.insert(0, ".")
from scrapers.base_scraper import BaseScraper

class Dumper(BaseScraper):
    @property
    def platform_name(self): return "Dumper"
    def login(self): return True
    def get_fare(self, p, d): pass

def main():
    d = Dumper(headless=True)
    d.start_driver()
    
    print("Dumping Uber...")
    d.driver.get("https://m.uber.com")
    time.sleep(5)
    with open("uber_source.html", "w", encoding="utf-8") as f:
        f.write(d.driver.page_source)

    print("Dumping Ola...")
    d.driver.get("https://book.olacabs.com")
    time.sleep(5)
    with open("ola_source.html", "w", encoding="utf-8") as f:
        f.write(d.driver.page_source)

    d.quit_driver()
    print("Done!")

if __name__ == "__main__":
    main()
