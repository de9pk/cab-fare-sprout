"""
uber_scraper.py
───────────────
Scrapes fare estimates from m.uber.com (mobile web — simpler DOM than app).

Strategy:
  1. Try loading saved cookies → check if already logged in
  2. If not logged in → use env vars to log in via OTP flow
  3. Input pickup + destination → extract fare card data
  4. Parse fare range & ETA → return structured result

NOTE: Uber's DOM changes frequently. Selectors are as of early 2024.
      If scraping fails, enable headless=False to watch what's happening,
      then update the XPath/CSS selectors below.
"""

import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from scrapers.base_scraper import BaseScraper


# ── Selectors (update these if Uber changes their HTML) ────────────────────────
class UberSelectors:
    BASE_URL         = "https://m.uber.com"
    LOGIN_URL        = "https://m.uber.com/go/login"

    # Login page
    PHONE_INPUT      = '#PHONE_NUMBER_or_EMAIL_ADDRESS'
    NEXT_BTN         = 'button[data-testid="forward-button"]'
    OTP_INPUT        = 'input[name="verificationCode"]'
    PASSWORD_INPUT   = 'input[name="password"]'

    # Home / ride booking
    # Uber changed UI: inputs are on the home page directly.
    PICKUP_INPUT     = 'input[aria-label="Search for a location"]'
    DEST_INPUT       = 'input[aria-label="Search for a location"]'
    SEARCH_BTN       = 'button[aria-label="Search"]'

    # Fare results
    FARE_CARD        = '[data-testid="product-selector-card"]'
    FARE_PRICE       = '[data-testid="price-badge"]'
    FARE_ETA         = '[data-testid="product-time"]'
    FARE_NAME        = '[data-testid="product-name"]'

    # Logged-in check
    LOGGED_IN_CHECK  = 'input[aria-label="Search for a location"]'


class UberScraper(BaseScraper):

    @property
    def platform_name(self) -> str:
        return "Uber"

    # ── Login ──────────────────────────────────────────────────────────────────

    def login(self) -> bool:
        """
        Attempt login using:
          1. Saved cookies (preferred)
          2. Env var credentials (phone/password)
        Returns True if logged in successfully.
        """
        if not self.driver:
            self.start_driver()

        # Try cookie login first
        if self.cookies_exist():
            self.logger.info("Found saved cookies — attempting cookie login...")
            self.load_cookies(UberSelectors.BASE_URL)
            if self._is_logged_in():
                self.logger.info("✅ Cookie login successful!")
                return True
            self.logger.warning("Cookies expired — falling back to credential login")

        # Credential login
        phone = os.getenv("UBER_PHONE", "")
        password = os.getenv("UBER_PASSWORD", "")

        return self._credential_login(phone, password)

    def _is_logged_in(self) -> bool:
        try:
            self.driver.get(UberSelectors.BASE_URL)
            self._human_delay(2, 3)
            self.driver.find_element(By.CSS_SELECTOR, UberSelectors.LOGGED_IN_CHECK)
            return True
        except NoSuchElementException:
            return False

    def _credential_login(self, phone: str, password: str) -> bool:
        """Login with phone + password, or fully manual if no env vars."""
        try:
            self.driver.get(UberSelectors.LOGIN_URL)
            self._human_delay(2, 3)

            if phone:
                # Enter phone number
                phone_field = self._wait_for(By.CSS_SELECTOR, UberSelectors.PHONE_INPUT)
                self._type_slowly(phone_field, phone)
                self._human_delay(0.5, 1)

                # Click Next
                self._click(By.CSS_SELECTOR, UberSelectors.NEXT_BTN)
                self._human_delay(2, 3)

                # Try password field first
                try:
                    pwd_field = self._wait_for(By.CSS_SELECTOR, UberSelectors.PASSWORD_INPUT, timeout=5)
                    self._type_slowly(pwd_field, password)
                    self._click(By.CSS_SELECTOR, UberSelectors.NEXT_BTN)
                    self._human_delay(3, 5)
                except TimeoutException:
                    pass

            self.logger.warning(
                "⚠️  Please complete the login (phone/password/OTP) manually in the browser. "
                "You have 120 seconds..."
            )
            
            # Wait up to 120s for user to enter everything
            for _ in range(120):
                if self._is_logged_in():
                    self.save_cookies()
                    self.logger.info("✅ Credential login successful!")
                    return True
                time.sleep(1)

            self.logger.error("❌ Login failed or timed out.")
            return False

        except Exception as e:
            self.logger.error(f"Login error: {e}")
            self._take_screenshot("login_error")
            return False

    # ── Fare scraping ──────────────────────────────────────────────────────────

    def get_fare(self, pickup: str, destination: str) -> dict:
        """
        Scrape Uber fare for the given pickup → destination.
        Returns a structured fare result dict.
        """
        if not self.driver:
            self.start_driver()

        try:
            self.driver.get(UberSelectors.BASE_URL)
            self._human_delay(2, 3)

            # Wait for inputs to appear
            self._wait_for(By.CSS_SELECTOR, UberSelectors.PICKUP_INPUT)
            self._human_delay(1, 2)
            
            # Enter pickup location
            # Fetch elements multiple times due to React re-rendering causing stale elements
            inputs = self.driver.find_elements(By.CSS_SELECTOR, UberSelectors.PICKUP_INPUT)
            if len(inputs) < 2:
                return self._build_error_result("Could not find pickup/dropoff inputs on Uber")
                
            inputs[0].click()
            self._human_delay(1, 1.5)
            
            # Refetch before typing
            inputs = self.driver.find_elements(By.CSS_SELECTOR, UberSelectors.PICKUP_INPUT)
            if len(inputs) > 0:
                self._type_slowly(inputs[0], pickup)
            self._human_delay(2, 3)
            # Fetch again in case it got stale while typing
            inputs = self.driver.find_elements(By.CSS_SELECTOR, UberSelectors.PICKUP_INPUT)
            if len(inputs) >= 2:
                inputs[0].send_keys(Keys.ENTER)
            self._human_delay(2, 3)

            # Enter destination
            inputs = self.driver.find_elements(By.CSS_SELECTOR, UberSelectors.DEST_INPUT)
            if len(inputs) >= 2:
                inputs[1].click()
                self._human_delay(1, 1.5)
                # Refetch before typing
                inputs = self.driver.find_elements(By.CSS_SELECTOR, UberSelectors.DEST_INPUT)
                if len(inputs) >= 2:
                    self._type_slowly(inputs[1], destination)
                self._human_delay(2, 3)
                # Fetch again
                inputs = self.driver.find_elements(By.CSS_SELECTOR, UberSelectors.DEST_INPUT)
                if len(inputs) >= 2:
                    inputs[1].send_keys(Keys.ENTER)
            
            self._human_delay(2, 3)
            
            # Click Search button
            try:
                self._click(By.CSS_SELECTOR, UberSelectors.SEARCH_BTN, timeout=5)
            except:
                pass # If it auto-searches or there is no search button
                
            self._human_delay(3, 5)  # Wait for fare cards to load

            # Parse fare results
            return self._parse_fares()

        except TimeoutException:
            self._take_screenshot("fare_timeout")
            return self._build_error_result("Timeout waiting for Uber fare results")
        except Exception as e:
            self._take_screenshot("fare_error")
            return self._build_error_result(str(e))

    def _parse_fares(self) -> dict:
        """Extract the cheapest fare from Uber's product cards."""
        soup = self._get_page_soup()

        # Find all fare/product cards
        cards = soup.select(UberSelectors.FARE_CARD)

        if not cards:
            # Fallback: try reading any price text visible on page
            return self._fallback_parse(soup)

        best_fare = None
        best_min = float("inf")

        for card in cards:
            try:
                price_el = card.select_one(UberSelectors.FARE_PRICE)
                eta_el   = card.select_one(UberSelectors.FARE_ETA)
                name_el  = card.select_one(UberSelectors.FARE_NAME)

                price_text = price_el.get_text(strip=True) if price_el else ""
                eta_text   = eta_el.get_text(strip=True)   if eta_el   else "N/A"
                name_text  = name_el.get_text(strip=True)  if name_el  else "UberGo"

                if not price_text:
                    continue

                fare_min, fare_max = self._parse_fare_range(price_text)

                if fare_min < best_min:
                    best_min = fare_min
                    best_fare = {
                        "platform":  self.platform_name,
                        "fare":      price_text,
                        "fare_min":  fare_min,
                        "fare_max":  fare_max,
                        "eta":       eta_text,
                        "ride_type": name_text,
                        "status":    "success",
                        "error_msg": "",
                    }
            except Exception as e:
                self.logger.debug(f"Error parsing card: {e}")
                continue

        if best_fare:
            return best_fare

        return self._build_error_result("Could not parse any Uber fare cards")

    def _fallback_parse(self, soup) -> dict:
        """Fallback: search for any price-like text on the page."""
        import re
        text = soup.get_text()
        matches = re.findall(r"₹\s*\d+(?:[–\-]\d+)?", text)
        if matches:
            fare_text = matches[0]
            fare_min, fare_max = self._parse_fare_range(fare_text)
            return {
                "platform":  self.platform_name,
                "fare":      fare_text,
                "fare_min":  fare_min,
                "fare_max":  fare_max,
                "eta":       "N/A",
                "ride_type": "UberGo",
                "status":    "success",
                "error_msg": "(fallback parser used)",
            }
        return self._build_error_result("No fare data found on Uber page")
