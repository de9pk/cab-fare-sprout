import sys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

sys.path.insert(0, ".")
from scrapers.base_scraper import BaseScraper

class TestScraper(BaseScraper):
    @property
    def platform_name(self): return "Test"
    def login(self): return True
    def get_fare(self, p, d): pass

def test_uber():
    s = TestScraper(headless=True)
    s.start_driver()
    s.driver.get("https://m.uber.com")
    time.sleep(4)
    
    inputs = s.driver.find_elements(By.CSS_SELECTOR, 'input[aria-label="Search for a location"]')
    print(f"Uber found {len(inputs)} inputs")
    if len(inputs) >= 2:
        pickup_input = inputs[0]
        pickup_input.clear()
        pickup_input.send_keys("Hawa Mahal, Jaipur, Rajasthan")
        time.sleep(3)
        pickup_input.send_keys(Keys.ENTER)
        time.sleep(2)
        
        dest_input = inputs[1]
        dest_input.clear()
        dest_input.send_keys("Jaipur International Airport")
        time.sleep(3)
        dest_input.send_keys(Keys.ENTER)
        time.sleep(2)
        
        s.driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Search"]').click()
        time.sleep(5)
        
        print("Uber fare page html:")
        html = s.driver.page_source
        if "₹" in html:
            print("Found ₹ symbol in HTML!")
        else:
            print("No fare found yet.")
    s.quit_driver()

def test_ola():
    s = TestScraper(headless=True)
    s.start_driver()
    s.driver.get("https://book.olacabs.com")
    print("Waiting 15 seconds for Ola to load...")
    time.sleep(15)
    print("Ola inputs:")
    inputs = s.driver.find_elements(By.TAG_NAME, 'input')
    for inp in inputs:
        print("Ola input:", inp.get_attribute("placeholder"), inp.get_attribute("class"))
    s.quit_driver()

def test_rapido():
    s = TestScraper(headless=True)
    s.start_driver()
    s.driver.get("https://rapido.bike")
    time.sleep(4)
    
    # Based on elements.txt
    try:
        p_input = s.driver.find_element(By.CSS_SELECTOR, 'input[placeholder*="Pickup"]')
        p_input.send_keys("Hawa Mahal, Jaipur")
        time.sleep(2)
        p_input.send_keys(Keys.ARROW_DOWN)
        p_input.send_keys(Keys.ENTER)
        time.sleep(1)
        
        d_input = s.driver.find_element(By.CSS_SELECTOR, 'input[placeholder*="Drop"]')
        d_input.send_keys("Jaipur International Airport")
        time.sleep(2)
        d_input.send_keys(Keys.ARROW_DOWN)
        d_input.send_keys(Keys.ENTER)
        time.sleep(1)
        
        btn = s.driver.find_element(By.XPATH, "//button[contains(text(), 'Book Ride') or contains(text(), 'Search')]")
        btn.click()
        time.sleep(5)
        
        print("Rapido HTML has ₹:", "₹" in s.driver.page_source)
    except Exception as e:
        print("Rapido Error:", e)
    s.quit_driver()

if __name__ == "__main__":
    print("--- Testing Uber ---")
    test_uber()
    print("--- Testing Ola ---")
    test_ola()
    print("--- Testing Rapido ---")
    test_rapido()
