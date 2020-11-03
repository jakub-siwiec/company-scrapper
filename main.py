from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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


driver.close()