from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from decouple import config
import time


class Linkedinwebsite:
    def __init__(self):
        self.PATH = "./chromedriver"
        self.driver = webdriver.Chrome(self.PATH)
        self.username = config('LINKEDIN_EMAIL')
        self.password = config('LINKEDIN_PASSWORD')
        self._login()

    def _login(self):
        """Logins to Linkedin
        """
        self.driver.get("https://www.linkedin.com/login")
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

    def _go_company_site(self, linkedin_company_profile_url):
        """Goes to the company website.

        Args:
            linkedin_company_profile_url (string): Company's LinkedIn profile full url.
        """
        self.driver.get(linkedin_company_profile_url)

    def _copy_button_website_link(self):
        """Copies website link from company's profile page if the link exists.

        Returns:
            string or None: Website url. None if no website url.
        """
        try:
            link = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Visit website")))
            return link.get_attribute("href")
        except:
            return None

    def _copy_details_website_link(self):
        """Get address from details of the website if visible.

        Returns:
            string oe None: Website url. None if no website url.
        """
        try:
            link = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "http")))
            return link.get_attribute("href")
        except:
            return None

    def get_website_link(self, linkedin_company_profile_url):
        """Goes to the company's webiste and gets a website url if exists. If not returns None.

        Args:
            linkedin_company_profile_url (string): Company's LinkedIn profile full url.

        Returns:
            string: Website url. None if no website url.
        """
        self._go_company_site(linkedin_company_profile_url)
        res = self._copy_button_website_link()
        if res is None:
            res = self._copy_details_website_link()
        return res

    def close(self):
        """Quits selenium session
        """
        self.driver.quit()
