import sys
import os
import json

# Add project root to path
sys.path.insert(0, ".")

from scrapers.uber_scraper   import UberScraper, UberSelectors
from scrapers.ola_scraper    import OlaScraper, OlaSelectors
from scrapers.rapido_scraper import RapidoScraper, RapidoSelectors
from utils.location_helper   import get_all_locations

def test():
    locations = get_all_locations()
    pickup = locations["🏛️  Hawa Mahal"]
    dest = locations["✈️  Jaipur International Airport"]
    
    print(f"Testing pickup: {pickup} to dest: {dest}")
    
    print("--- UBER ---")
    u = UberScraper(headless=True)
    res_u = u.get_fare(pickup, dest)
    print(json.dumps(res_u, indent=2))
    u.quit_driver()
    
    print("--- OLA ---")
    o = OlaScraper(headless=True)
    res_o = o.get_fare(pickup, dest)
    print(json.dumps(res_o, indent=2))
    o.quit_driver()

    print("--- RAPIDO ---")
    r = RapidoScraper(headless=True)
    res_r = r.get_fare(pickup, dest)
    print(json.dumps(res_r, indent=2))
    r.quit_driver()

if __name__ == "__main__":
    test()
