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
        self.get_website_link()

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

    def get_website_link(self):
        button_link = self._button_link()
        print(button_link)

    def close(self):
        self.driver.close()


x = Domain()
x.close()
