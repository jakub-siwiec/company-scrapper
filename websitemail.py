from extract_emails import EmailExtractor
from extract_emails.browsers import BrowserInterface

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Websitemail(BrowserInterface):
    def __init__(self):
        ch_options = Options()
        self._driver = webdriver.Chrome(
            options=ch_options, executable_path="./chromedriver",
        )

    def close(self):
        self._driver.quit()

    def get_page_source(self, url: str) -> str:
        print(url)
        self._driver.get(url)
        return self._driver.page_source


def get_website_emails(website_root_address):
    email_list = []
    try:
        with Websitemail() as browser:
            email_extractor = EmailExtractor(
                website_root_address, browser, depth=2, max_links_from_page=30)
            emails = email_extractor.get_emails()

        for email in emails:
            email_address = email.as_dict()
            print(email_address["email"])
            email_list.append(email_address["email"])

        return ', '.join(email_list)
    except:
        return ""
