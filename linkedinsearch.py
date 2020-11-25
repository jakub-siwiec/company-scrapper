from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from decouple import config
import pandas as pd
import time


class Linkedinsearch:
    def __init__(self):
        """LinkedIn session object.

        The procedure:

        1. You initiate the object (it opens the browser, login to Linkedin, create csv file etc.).
        2. You insert the company's name in the Linkedin search with search method/You go to the list of people signed with the company with company_people_list method.
        3. You scrap the results with scrap/scrap_and_update_csv method. If you choose the former one you want to save the result in a certain way (to csv or another way with e.g. get_result).
        4. Close driver.
        """
        self.PATH = "./chromedriver"
        idx = config("LINKEDIN_CSV_FILE_OUTPUT").index(".csv")
        timestring = time.strftime("%Y%m%d%H%M%S")
        self.FILE = config("LINKEDIN_CSV_FILE_OUTPUT")[
            :idx] + timestring + config("LINKEDIN_CSV_FILE_OUTPUT")[idx:]
        self.csv_sep = "$"
        self.driver = webdriver.Chrome(self.PATH)
        self.results = []
        self.pagination_max = 5
        self.pagination_session = 0
        self.column_names = ["Name", 'Company',
                             "Description", "Location", "Link"]
        self.username = config('LINKEDIN_EMAIL')
        self.password = config('LINKEDIN_PASSWORD')

        self._create_csv()
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

    def search(self, search_company):
        """Searches the company in Linkedin search.

        Args:
            search_company (string): Name of the company to search.

        Returns:
            boolean: True if there is it proceeded to the search list, False if it didn't.
        """
        self.results.append({
            "company": search_company,
            "list": []
        })
        try:
            search_field = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//div[@id='global-nav-search']//input[@aria-label='Search']")))
            search_field.clear()
            search_field.send_keys(search_company)
            search_field.send_keys(Keys.ENTER)
            return True
        except:
            return False

    def company_people_list(self, search_company, company_linkedin_page):
        """Gets the list of people currently working in the company through LinkedIn company page.

        Args:
            search_company (string): Name of the company to search.
            company_linkedin_page (string): Full company LinkedIn address of the format https://www.linkedin.com/company/[company-user-name]/.

        Returns:
            boolean: True if there is it proceeded to the list, False if it didn't.
        """
        self.results.append({
            "company": search_company,
            "list": []
        })
        self.driver.get(company_linkedin_page)
        try:
            link_people_list = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "employees on LinkedIn")))
            link_people_list.click()
            return True
        except:
            try:
                link_people_list = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "employee on LinkedIn")))
                link_people_list.click()
                return True
            except:
                return False

    def _scroll_to_bottom(self):
        """Scrolls the page to the bottom by pressing down key.
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
        if self.pagination_session < self.pagination_max:
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

    def get_results(self):
        """Get results.

        Returns:
            List: List of dictionaries.
        """
        return self.results

    def get_last_to_df(self):
        """Creates an output form in the form of columns in a particular order with the particular information.

        Returns:
            Dataframe: Pandas dataframe object.
        """
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

    def scrap(self):
        """Scraps the data paginating.
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

    def scrap_and_update_csv(self):
        """Scraps the data paginating in the meantime and saves it.
        """
        self.scrap()
        self.update_csv()

    def close(self):
        """Closes the selenium session.
        """
        self.driver.close()
