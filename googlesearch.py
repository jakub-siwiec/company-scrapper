from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


class Domain:
    def __init__(self):
        self.PATH = "./chromedriver"
        self.driver = webdriver.Chrome(self.PATH)
        self.driver.get("https://google.com")
        self.search_company = "Google search"

        # ACTION
        # time.sleep(5)
        self._close_google_privacy_modal()
        self.search("Goldman Sachs")
        # self.search("ufrh3u834832ruy3yy23h")
        self.get_website_link()
        b = self._get_search_results()
        c = self._convert_search_results_to_dict(b)
        print(c)
        a = input("hehehe")

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

    def search(self, search_phrase):
        """Search initial page or later one

        Args:
            search_keywords (string): Keywords to search
        """
        input_element = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.NAME, "q")))
        input_element.clear()
        input_element.send_keys(search_phrase)
        input_element.send_keys(Keys.RETURN)
        assert "No results found." not in self.driver.page_source
        self.driver.implicitly_wait(10)

    def _scroll_to_bottom(self):
        """Scrolls the page to the bottom by pressing down key.
        """
        time.sleep(2)
        body = self.driver.find_element_by_css_selector('body')
        while self.driver.execute_script('return ((window.innerHeight + window.pageYOffset) >= document.body.offsetHeight - 2);') == False:
            body.send_keys(Keys.PAGE_DOWN)
        time.sleep(2)

    def _button_link(self):
        """Get the link to the button of the website (my chromedriver browser is in Polish, change "Strona" for your language)

        Returns:
            string: link to the website
        """
        try:
            details_buttons = WebDriverWait(self.driver, 5).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "ab_button")))

            for item in details_buttons:
                if item.text == "Strona":
                    return item.get_attribute("href")
        except:
            return None

        return None

    def _get_search_results(self):
        """Get all the results in the page for particular search

        Returns:
            list: list of selenium objects. None if no results
        """
        try:
            self._scroll_to_bottom()
            full_results_list = WebDriverWait(self.driver, 5).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "rc")))
            return full_results_list
        except:
            return None

    def _convert_search_results_to_dict(self, full_results_list):
        """Converts results to a list of dictionaries

        Args:
            full_results_list (list): List of selenium objects

        Returns:
            list: List of dictionaries with links and titles of the search results
        """
        if full_results_list != None:
            list_link_title = []
            for result in full_results_list:
                link = result.find_element_by_tag_name("a")
                title = result.find_element_by_tag_name("h3")
                result_output = {
                    "link": link.get_attribute("href"),
                    "title": title.text
                }
                list_link_title.append(result_output)
            return list_link_title
        else:
            return None

    def get_website_link(self):
        button_link = self._button_link()
        print(button_link)

    def close(self):
        self.driver.close()


x = Domain()
x.close()
