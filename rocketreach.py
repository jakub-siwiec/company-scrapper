from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import re


class Rocketreach:
    def __init__(self, search_company):
        self.PATH = "./chromedriver"
        self.driver = webdriver.Chrome(self.PATH)
        self.driver.get("https://google.com")
        self.search_company = search_company

        # ACTION

        self._close_google_privacy_modal()
        self._initial_search()

        self.results = self._print_google_rocketreach_results(
            self._get_all_google_page_results())

        self.driver.close()

    def _close_google_privacy_modal(self):
        """Close initial Google privacy modal window
        """
        WebDriverWait(self.driver, 5).until(
            EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe"))
        )
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[@id='introAgreeButton']/span"))
        ).click()

    def _initial_search(self):
        """Search initial page

        Args:
            search_keywords (string): Keywords to search
        """
        input_element = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.NAME, "q")))
        input_element.send_keys("{} email format".format(self.search_company))
        input_element.send_keys(Keys.RETURN)
        assert "No results found." not in self.driver.page_source
        self.driver.implicitly_wait(10)

    def _get_all_google_page_results(self):
        """Returns all the results from the google results

        Returns:
            List: Result elements with g class name
        """
        return self.driver.find_elements_by_class_name("g")

    def _print_google_rocketreach_results(self, links_list):
        pattern_list = [
            {
                "pattern": "used (.*?) of the time",
                "pattern_email": "\((.*?)\). Enter",
                "substring": False,
                "address_google": None
            },
            {
                "pattern": "\((.*?)\). Enter",
                "pattern_email": "1. (.*?) \(",
                "substring": False,
                "address_google": None
            },
        ]

        for link_content in links_list:
            link_content_text = link_content.text
            link_content_html = link_content.get_attribute("innerHTML")
            if "rocketreach.co" in link_content_html:
                # Uncover
                for pattern in pattern_list:
                    pattern_percentage = re.search(
                        pattern["pattern"], link_content_text)
                    pattern_email = re.search(
                        pattern["pattern_email"], link_content_text)
                    substring = False if pattern_percentage == None or pattern_email == None else True
                    pattern.update({"substring": substring})

                    if substring:
                        if float(pattern_percentage.group(1).replace("%", "")) >= 70:
                            pattern.update(
                                {"address_google": pattern_email.group(1)})
                        else:
                            pattern.update({"address_google": None})
                    else:
                        pattern.update({"address_google": None})

        return pattern_list

    def get_results(self):
        email_pattern = None
        for result in self.results:
            if result["substring"] == True:
                if result["address_google"] != None:
                    email_pattern = result["address_google"]
        return email_pattern
