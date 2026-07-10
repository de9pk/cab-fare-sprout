"""
debug_selectors.py
──────────────────
Run this script to test if selectors work on a specific platform.
Super useful when Uber/Ola/Rapido update their frontend and scraping breaks.

Usage:
  python debug_selectors.py --platform uber
  python debug_selectors.py --platform ola
  python debug_selectors.py --platform rapido
"""

import argparse
import sys
import time
from selenium.webdriver.common.by import By

# Add project root to path
sys.path.insert(0, ".")

from scrapers.uber_scraper   import UberScraper, UberSelectors
from scrapers.ola_scraper    import OlaScraper, OlaSelectors
from scrapers.rapido_scraper import RapidoScraper, RapidoSelectors


def debug_uber():
    print("\n🔍 Testing Uber selectors...")
    s = UberScraper(headless=False)
    s.start_driver()

    print(f"  → Opening {UberSelectors.BASE_URL}")
    s.driver.get(UberSelectors.BASE_URL)
    s._human_delay(3, 4)

    # Test each selector
    selectors_to_test = {
        "Where To Button": UberSelectors.WHERE_TO_BTN,
        "Pickup Input":    UberSelectors.PICKUP_INPUT,
        "Destination":     UberSelectors.DEST_INPUT,
        "Fare Card":       UberSelectors.FARE_CARD,
    }

    for name, sel in selectors_to_test.items():
        try:
            els = s.driver.find_elements(By.CSS_SELECTOR, sel)
            status = f"✅ Found {len(els)} element(s)" if els else "⚠️ Not found"
        except Exception as e:
            status = f"❌ Error: {e}"
        print(f"  {name}: {status}")

    print("\n  📸 Saving screenshot to /tmp/uber_debug.png")
    s.driver.save_screenshot("/tmp/uber_debug.png")

    input("\n  Press Enter to close browser...")
    s.quit_driver()


def debug_ola():
    print("\n🔍 Testing Ola selectors...")
    s = OlaScraper(headless=False)
    s.start_driver()

    print(f"  → Opening {OlaSelectors.BASE_URL}")
    s.driver.get(OlaSelectors.BASE_URL)
    s._human_delay(3, 4)

    selectors_to_test = {
        "Pickup Input": OlaSelectors.PICKUP_INPUT,
        "Dest Input":   OlaSelectors.DEST_INPUT,
        "Ride Card":    OlaSelectors.RIDE_CARD,
    }

    for name, sel in selectors_to_test.items():
        try:
            els = s.driver.find_elements(By.CSS_SELECTOR, sel)
            status = f"✅ Found {len(els)} element(s)" if els else "⚠️ Not found"
        except Exception as e:
            status = f"❌ Error: {e}"
        print(f"  {name}: {status}")

    s.driver.save_screenshot("/tmp/ola_debug.png")
    input("\n  Press Enter to close browser...")
    s.quit_driver()


def debug_rapido():
    print("\n🔍 Testing Rapido selectors...")
    s = RapidoScraper(headless=False)
    s.start_driver()

    print(f"  → Opening {RapidoSelectors.BASE_URL}")
    s.driver.get(RapidoSelectors.BASE_URL)
    s._human_delay(3, 4)

    selectors_to_test = {
        "Pickup Input": RapidoSelectors.PICKUP_INPUT,
        "Dest Input":   RapidoSelectors.DEST_INPUT,
        "Ride Card":    RapidoSelectors.RIDE_CARD,
    }

    for name, sel in selectors_to_test.items():
        try:
            els = s.driver.find_elements(By.CSS_SELECTOR, sel)
            status = f"✅ Found {len(els)} element(s)" if els else "⚠️ Not found"
        except Exception as e:
            status = f"❌ Error: {e}"
        print(f"  {name}: {status}")

    s.driver.save_screenshot("/tmp/rapido_debug.png")
    input("\n  Press Enter to close browser...")
    s.quit_driver()


def print_page_elements(scraper, url: str):
    """Print all interactive elements found on a page — helps find correct selectors."""
    scraper.start_driver()
    scraper.driver.get(url)
    time.sleep(3)

    print("\n  📋 All input elements:")
    inputs = scraper.driver.find_elements(By.TAG_NAME, "input")
    for el in inputs:
        t  = el.get_attribute("type") or "text"
        ph = el.get_attribute("placeholder") or ""
        nm = el.get_attribute("name") or ""
        cl = (el.get_attribute("class") or "")[:60]
        print(f"    input[type={t}] placeholder='{ph}' name='{nm}' class='{cl}'")

    print("\n  📋 All buttons:")
    btns = scraper.driver.find_elements(By.TAG_NAME, "button")
    for btn in btns[:15]:
        txt = btn.text[:40] or "[no text]"
        cl  = (btn.get_attribute("class") or "")[:60]
        print(f"    button '{txt}' class='{cl}'")

    scraper.quit_driver()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Debug cab scraper selectors")
    parser.add_argument("--platform", choices=["uber", "ola", "rapido", "all"], default="all")
    parser.add_argument("--elements", action="store_true", help="Print all page elements")
    args = parser.parse_args()

    print("=" * 60)
    print("  Cab Fare Comparator — Selector Debugger")
    print("=" * 60)

    if args.elements:
        url_map = {
            "uber":   "https://m.uber.com",
            "ola":    "https://book.olacabs.com",
            "rapido": "https://rapido.bike",
        }
        for plat, url in url_map.items():
            if args.platform in (plat, "all"):
                scraper_map = {"uber": UberScraper, "ola": OlaScraper, "rapido": RapidoScraper}
                s = scraper_map[plat](headless=True)
                print(f"\n{'='*40}\n  {plat.upper()} — {url}\n{'='*40}")
                print_page_elements(s, url)
    else:
        if args.platform in ("uber", "all"):    debug_uber()
        if args.platform in ("ola", "all"):     debug_ola()
        if args.platform in ("rapido", "all"):  debug_rapido()

    print("\n✅ Debug complete!")
