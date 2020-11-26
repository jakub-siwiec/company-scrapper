from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import tldextract


class Sitecrawler:
    def __init__(self):
        self.collected_links = []
        self.PATH = "./chromedriver"
        self.driver = webdriver.Chrome(self.PATH)

    def _get_all_links(self):
        """Get all links from the website.

        Returns:
            list: All a tags.
        """
        a_links = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "a")))
        return a_links

    def _get_domain(self, url):
        """Extracts domain name from url.

        Args:
            url (string): String url address.

        Returns:
            string: Domain address (with suffix).
        """
        info_url = tldextract.extract(url)
        return info_url.registered_domain

    def _append_link(self, link, session_object, link_list_type=True):
        """Append link to the list of links. Internal links go to internal category, external to the external category. Passed link is checked whether there is a duplicate.

        Args:
            link (string): Link to add to the list.
            session_object (dictionary): Dictionary with the keys site-address (string value), internal-links (list of strings), external-links (list of strings).
            link_list_type (bool, optional): If true then internal, if false external list. Defaults to True.
        """
        link_list = session_object["internal-links"] if link_list_type else session_object["external-links"]
        if link not in link_list:
            if link_list_type == True:
                session_object["internal-links"].append(link)
            else:
                session_object["external-links"].append(link)

    def _assign_links(self, site_address, links, session_object):
        """Get href addresses from links, assign to the right category (internal or external).

        Args:
            site_address (string): Root site address we obtain links from.
            links (list): List of selenium webdriver objects of the elements from a tag.
            session_object (dictionary): Dictionary with the keys site-address (string value), internal-links (list of strings), external-links (list of strings).
        """
        main_domain = self._get_domain(site_address)
        for link in links:
            current_link = link.get_attribute("href")
            if current_link is not None:
                if self._get_domain(current_link) == main_domain:
                    self._append_link(current_link, session_object)
                else:
                    self._append_link(current_link, session_object, False)

    def _go_site(self, site_address):
        """Go to the root address.

        Args:
            site_address (string): Root site address we obtain links from.
        """
        self.driver.get(site_address)
        time.sleep(3)

    def get_links(self):
        """Get list of results

        Returns:
            list: List of dictionaries with the keys site-address (string value), internal-links (list of strings), external-links (list of strings).
        """
        return self.collected_links

    def go_and_discover_links(self, site_address):
        """Main method to go to the certain address, get the links and append them to the list.

        Args:
            site_address (string): Root site address we obtain links from.
        """
        session_object = {
            "site-address": site_address,
            "internal-links": [],
            "external-links": []
        }
        self._go_site(site_address)
        links = self._get_all_links()
        self._assign_links(site_address, links, session_object)
        self.collected_links.append(session_object)

    def close(self):
        """Quit driver
        """
        self.driver.quit()
