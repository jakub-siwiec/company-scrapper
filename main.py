from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import re

PATH = "./chromedriver"
driver = webdriver.Chrome(PATH)

driver.get("https://google.com")

# Close privacy modal

WebDriverWait(driver, 5).until(
    EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe"))
)
WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.XPATH, "//*[@id='introAgreeButton']/span"))
).click()

# Search

input_element = WebDriverWait(driver, 5).until(
    EC.visibility_of_element_located((By.NAME, "q"))
)
input_element.send_keys("Otus Capital Management Limited email format")
input_element.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
driver.implicitly_wait(10)

# Get emails from rocketreach


def rocket_in_google_results(links_list):
    for link_content in links_list:
        link_content_text = link_content.text
        link_content_html = link_content.get_attribute("innerHTML")
        pattern_list = [
            {"pattern": "used (.*?) of the time", "pattern_email": "\((.*?)\). Enter"},
            {"pattern": "\((.*?)\). Enter", "pattern_email": "1. (.*?) \("},
        ]
        if "rocketreach.co" in link_content_html:
            # Uncover
            for pattern in pattern_list:
                pattern_percentage = re.search(pattern["pattern"], link_content_text)
                pattern_email = re.search(pattern["pattern_email"], link_content_text)
                substring = False if pattern_percentage == None else True
                pattern.update({"substring": substring})

                if substring:
                    if float(pattern_percentage.group(1).replace("%", "")) >= 70:
                        pattern.update({"address_google": pattern_email.group(1)})
                    else:
                        pattern.update({"address_google": None})
                else:
                    pattern.update({"address_google": None})
            return pattern_list


links_list = driver.find_elements_by_class_name("g")

res = rocket_in_google_results(links_list)

print(res)


driver.close()