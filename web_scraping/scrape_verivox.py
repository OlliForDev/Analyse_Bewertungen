import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from utilities import insert_provider, insert_ratings, get_provider_details, get_all_ratings
from settings import CHROME_DRIVER_PATH

# If chromedriver is in your PATH, you can use this:
#driver = webdriver.Chrome()

service = Service(CHROME_DRIVER_PATH)
# If you didn’t add ChromeDriver to PATH, specify the full path:
driver = webdriver.Chrome(service=service)


print('--------------START--------------')
# Open a webpage
driver.get('https://www.verivox.de/anbieter/sw-karlsruhe/')
# Perform any actions with Selenium
# allow cookies
time.sleep(2)
ele_cookies_btn = driver.find_element(By.ID, 'uc-btn-accept-banner')
print(ele_cookies_btn.text)
ele_cookies_btn.click()
time.sleep(2)
#expand costumer reviews
ele_label_expand_cust_reviews = driver.find_element(By.CSS_SELECTOR, "label[for='expand-reviews']")
ele_label_expand_cust_reviews.click()
time.sleep(2)

while True:
    try:
        # Wait until the "Show More" button is clickable
        ele_load_more_reviews = driver.find_element(By.XPATH, "//div[@class='load-more']")
        # Click the "Show More" button
        ele_load_more_reviews.click()
        # Optionally, add a short pause to wait for the page to load more content
        time.sleep(2)  # Adjust the time if necessary
    except:
        # If the button is not found or clickable, break the loop
        print("No more 'Show More' buttons found.")
        break

time.sleep(2)
# Once all content is loaded, get the page source
page_source = driver.page_source
# Close the Selenium WebDriver
driver.quit()
# Parse the page source with BeautifulSoup
soup = BeautifulSoup(page_source, "html.parser")

provider_details = get_provider_details(soup)

print(provider_details)

insert_provider(provider_name=provider_details['name'], 
                foundation_year=provider_details['year_of_foundation'], 
                number_of_employees=provider_details['number_of_employees'],
                number_of_customer=provider_details['number_of_customer'],
                revenue=provider_details['revenue'],
                post_code=provider_details['post_code'])

# Scrape all ratings
all_ratings = get_all_ratings(soup)

for rating in all_ratings:
    insert_ratings(title=rating['title'],
                scoring_price=rating['scoring_price'],
                scoring_provider_change=rating['scoring_provider_change'],
                scoring_service=rating['scoring_service'],
                date_of_order=rating['date_of_order'],
                date_of_change=rating['date_of_change'],
                provider=provider_details['name']
                )
print('--------------END----------------')