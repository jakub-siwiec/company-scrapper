from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from decouple import config
import time
"""
PATH = "./chromedriver"
driver = webdriver.Chrome(PATH)
driver.get("https://www.linkedin.com/login")
a = input("kk")

# LOGIN

driver.find_element_by_id('username').send_keys(config('LINKEDIN_EMAIL'))
driver.find_element_by_id('password').send_keys(config('LINKEDIN_PASSWORD'))
driver.find_element_by_xpath(
    "//button[@data-litms-control-urn='login-submit']").click()
b = input("bb")

# SEARCH

search = driver.find_element_by_xpath(
    "//div[@id='global-nav-search']//input[@aria-label='Search']")
search.send_keys("Orchard Global Asset Management LLP")
search.send_keys(Keys.ENTER)
c = input("ccc")

# GET RESULTS

results = []
body = driver.find_element_by_css_selector('body')

while True:
    while driver.execute_script(
            'return ((window.innerHeight + window.pageYOffset) >= document.body.offsetHeight - 2);') == False:
        body.send_keys(Keys.PAGE_DOWN)

    try:
        next_button = driver.find_element_by_xpath(
            "//button[@aria-label='Next']")
        time.sleep(2)
        res_i = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//*[@data-test-search-result='PROFILE']")))
        print("Length: ", len(res_i))
        print("0th element: ", res_i[0])
        print("0th element text: ", res_i[0].text)
        for i in res_i:
            results.append(i.text)
        # NEXT PAGE

        if next_button.is_enabled():
            time.sleep(2)
            next_button.click()
            time.sleep(2)
        else:
            break
    except:
        pass

e = input("eee")
print("--------")
# PRINT RESULTS

print(results)


driver.close()

"""


class Linkedin:
    def __init__(self):
        self.PATH = "./chromedriver"
        self.driver = webdriver.Chrome(self.PATH)
        self.results = {
            "company": None,
            "list": []
        }
        self.username = config('LINKEDIN_EMAIL')
        self.password = config('LINKEDIN_PASSWORD')

        self.driver.get("https://www.linkedin.com/login")
        self._login()

    def _login(self):
        username_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "username")))
        password_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "password")))
        login_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//button[@data-litms-control-urn='login-submit']")))
        time.sleep(2)
        username_field.send_keys(self.username)
        password_field.send_keys(self.password)
        login_button.click()
        time.sleep(5)

    def search(self, search_company):
        self.results["company"] = search_company
        search_field = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//div[@id='global-nav-search']//input[@aria-label='Search']")))
        search_field.send_keys(search_company)
        search_field.send_keys(Keys.ENTER)

    def scrap(self):
        """Script for scrapping through the results
        """
        time.sleep(5)
        while True:
            body = self.driver.find_element_by_css_selector('body')

            # Scrolls to the bottom of the page
            while self.driver.execute_script('return ((window.innerHeight + window.pageYOffset) >= document.body.offsetHeight - 2);') == False:
                body.send_keys(Keys.PAGE_DOWN)

            # Scraps profiles
            try:
                time.sleep(2)
                result_page_items = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(
                    (By.XPATH, "//*[@data-test-search-result='PROFILE']")))
                for item in result_page_items:
                    profile_object = {
                        "name": None,
                        "link": None,
                        "description": None,
                        "location": None,
                        "full_text": item.text
                    }

                    try:
                        wrapper = item.find_element_by_class_name(
                            "search-result__info")
                        name_line = wrapper.find_element_by_tag_name("a")
                        profile_object["name"] = name_line.text.split("\n")[0]
                        profile_object["link"] = name_line.get_attribute(
                            "href")
                        profile_object["description"] = wrapper.find_element_by_css_selector(
                            "p.subline-level-1").text
                        profile_object["location"] = wrapper.find_element_by_css_selector(
                            "p.subline-level-2").text
                    except:
                        pass

                    self.results["list"].append(profile_object)

                # Goes to the next page unless there is no pagination or it is the last page
                pagination_present = len(self.driver.find_elements_by_class_name(
                    "artdeco-pagination__indicator")) > 0
                if pagination_present:
                    next_button = self.driver.find_element_by_xpath(
                        "//button[@aria-label='Next']")

                    if next_button.is_enabled():
                        time.sleep(2)
                        next_button.click()
                        time.sleep(2)
                    else:
                        time.sleep(2)
                        body.send_keys(Keys.CONTROL + Keys.HOME)
                        time.sleep(2)
                        break
                else:
                    time.sleep(2)
                    break
            except:
                pass

    def get_results(self):
        return self.results

    def close_linkedin(self):
        self.driver.close()


x = Linkedin()
x.search("J.P. Morgan")
x.scrap()
print(x.get_results())
x.close_linkedin()
