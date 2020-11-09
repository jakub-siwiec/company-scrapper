from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from decouple import config
import pandas as pd
import time


class Linkedin:
    def __init__(self):
        self.PATH = "./chromedriver"
        self.FILE = config("LINKEDIN_CSV_FILE_OUTPUT")
        self.csv_sep = "$"
        self.driver = webdriver.Chrome(self.PATH)
        self.results = []
        self.pagination_session = 0
        self.column_names = ["Name", 'Company',
                             "Description", "Location", "Link"]
        self.username = config('LINKEDIN_EMAIL')
        self.password = config('LINKEDIN_PASSWORD')

        self._create_csv()
        self.driver.get("https://www.linkedin.com/login")
        self._login()

    def _login(self):
        """Logins to Linkedin
        """
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
        """Searches the company in Linkedin search.

        Args:
            search_company (string): Name of the company to search.
        """
        self.results.append({
            "company": search_company,
            "list": []
        })
        search_field = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//div[@id='global-nav-search']//input[@aria-label='Search']")))
        search_field.clear()
        search_field.send_keys(search_company)
        search_field.send_keys(Keys.ENTER)

    def _scroll_to_bottom(self):
        """Scrolls the page to the bottom by pressing down key.

        Returns:
            [type]: [description]
        """
        body = self.driver.find_element_by_css_selector('body')
        while self.driver.execute_script('return ((window.innerHeight + window.pageYOffset) >= document.body.offsetHeight - 2);') == False:
            body.send_keys(Keys.PAGE_DOWN)

    def _increment_pagination(self):
        """Adds one page.
        """
        self.pagination_session += 1

    def _reset_pagination_session(self):
        """Resets pagination counting to 0.
        """
        self.pagination_session = 0

    def _continue_paginating(self):
        """Outputs whether to continue the pagination

        Returns:
            boolean: True continue, false discontinue
        """
        if self.pagination_session < 5:
            return True
        else:
            return False

    def _paginate(self):
        """Serves the pagination of search result page. Goes to the next page unless there is no pagination or it is the last page.

        Returns:
            boolean: True if clicks next page, False if no pagination or reached the last page.
        """
        body = self.driver.find_element_by_css_selector('body')
        pagination_present = len(self.driver.find_elements_by_class_name(
            "artdeco-pagination__indicator")) > 0
        if pagination_present:
            next_button = self.driver.find_element_by_xpath(
                "//button[@aria-label='Next']")

            if next_button.is_enabled() and self._continue_paginating():
                self._increment_pagination()
                time.sleep(2)
                next_button.click()
                time.sleep(2)
                return True
            else:
                self._reset_pagination_session()
                time.sleep(2)
                body.send_keys(Keys.CONTROL + Keys.HOME)
                time.sleep(2)
                return False
        else:
            time.sleep(2)
            return False

    def _get_page_data(self):
        """Gets the results data.

        Returns:
            list: List of selenium objects containing results of the search.
        """
        time.sleep(2)
        result_page_items = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(
            (By.XPATH, "//*[@data-test-search-result='PROFILE']")))
        return result_page_items

    def _unpack_page_data(self, result_page_items):
        """Unpacks the list of selenium objects into an objects of strings. First use _get_page_data.

        Args:
            result_page_items (list): List of selenium objects. Use _get_page_data method to obtain it.
        """
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

            self.results[-1]["list"].append(profile_object)

    def scrap(self):
        """Scraps the data paginating in the meantime and saves it.
        """
        time.sleep(5)
        while True:
            try:
                self._scroll_to_bottom()
                result_page_items = self._get_page_data()
                self._unpack_page_data(result_page_items)
                click_next_page = self._paginate()
                if click_next_page == False:
                    break
            except:
                break
        self.update_csv()

    def get_results(self):
        """Get results.

        Returns:
            List: List of dictionaries.
        """
        return self.results

    def get_last_to_df(self):
        list_dict_to_df = []
        for item in self.results[-1]["list"]:
            dict_to_df = {}
            dict_to_df[self.column_names[0]] = item["name"]
            dict_to_df[self.column_names[1]] = self.results[-1]["company"]
            dict_to_df[self.column_names[2]] = item["description"]
            dict_to_df[self.column_names[3]] = item["location"]
            dict_to_df[self.column_names[4]] = item["link"]
            list_dict_to_df.append(dict_to_df)
        df = pd.DataFrame(list_dict_to_df)
        return df

    def _create_csv(self):
        """Create new csv file with columns.
        """
        df = pd.DataFrame(columns=self.column_names)
        df.to_csv(self.FILE, sep=self.csv_sep)

    def _save_to_csv(self, df):
        """Append a DataFrame to the file.
        """
        df.to_csv(self.FILE, sep=self.csv_sep,
                  mode='a', index=False, header=False)

    def update_csv(self):
        """Update csv file with the last company searched
        """
        df = self.get_last_to_df()
        self._save_to_csv(df)

    def close(self):
        """Closes the selenium session.
        """
        self.driver.close()
