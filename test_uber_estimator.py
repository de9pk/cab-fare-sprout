import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

options = Options()
options.add_argument("--headless=new")
options.add_argument("--window-size=1366,768")
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
driver = webdriver.Chrome(options=options)

driver.get("https://www.uber.com/in/en/price-estimate/")
time.sleep(4)

try:
    inputs = driver.find_elements(By.CSS_SELECTOR, "input[aria-label='Pickup location']")
    if len(inputs) > 0:
        p_input = inputs[0]
        driver.execute_script("arguments[0].scrollIntoView(true);", p_input)
        time.sleep(1)
        p_input.click()
        time.sleep(1)
        for c in "Hawa Mahal, Jaipur, Rajasthan":
            p_input.send_keys(c)
            time.sleep(0.05)
        time.sleep(2)
        p_input.send_keys(Keys.ARROW_DOWN)
        p_input.send_keys(Keys.ENTER)
        time.sleep(1)
        
    inputs = driver.find_elements(By.CSS_SELECTOR, "input[aria-label='Dropoff location']")
    if len(inputs) > 0:
        d_input = inputs[0]
        driver.execute_script("arguments[0].scrollIntoView(true);", d_input)
        time.sleep(1)
        d_input.click()
        time.sleep(1)
        for c in "Jaipur International Airport, Sanganer":
            d_input.send_keys(c)
            time.sleep(0.05)
        time.sleep(2)
        d_input.send_keys(Keys.ARROW_DOWN)
        d_input.send_keys(Keys.ENTER)
        time.sleep(4)
        
    print("HTML after entering locations captured.")
    html = driver.page_source
    
    with open("uber_estimator_fares.html", "w", encoding="utf-8") as f:
        f.write(html)
        
except Exception as e:
    print(e)
driver.quit()
