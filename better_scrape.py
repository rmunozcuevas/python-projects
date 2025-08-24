from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def open_rateyourmusic():
    # Setup Chrome options
    options = Options()
    options.add_argument("--start-maximized")  # open Chrome maximized
    options.add_argument("--disable-blink-features=AutomationControlled")  # optional, hides automation flag
    
    # Initialize Chrome driver (make sure chromedriver is installed and in PATH)
    driver = webdriver.Chrome(options=options)

    try:
        # Open rateyourmusic homepage
        driver.get("https://rateyourmusic.com")
        
        # Wait until the main page loads by checking the presence of the search icon (example)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "menu__item--search"))
        )
        
        print("Page Title:", driver.title)
        
    except Exception as e:
        print("Error:", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    open_rateyourmusic()
