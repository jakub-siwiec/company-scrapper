from googlesearch import Googlesearch
import re


class Googlemail:
    def __init__(self):
        self.google_search_session = Googlesearch()

    def _get_results_text(self, search_phrase, pages=1):
        """Obtain pages text from google search where we add the keywords email format to the searched company name.

        Args:
            search_phrase (string): Search phrase to insert in Google search bar. Don't need to be Google start page.
            pages (int, optional): Number of pages (pagination) to handle. Defaults to 1.

        Returns:
            string: Text from all the pages paginated.
        """
        return self.google_search_session.get_full_page_in_text(search_phrase + " email format", pages)

    def find_emails(self, search_phrase, pages=1):
        """Get emails and email patterns from the text results.

        Args:
            search_phrase (string): Search phrase to insert in Google search bar. Don't need to be Google start page.
            pages (int, optional): Number of pages (pagination) to handle. Defaults to 1.

        Returns:
            list: List of strings or tuples with the results. May require cleaning after.
        """
        results = []
        results_text = self._get_results_text(search_phrase, pages=1)
        regex_phrase = '(([A-Z0-9._%+-{}]|first_initial\s|first\s|last_initial\s|last\s|\'.\'\s|\'-\'\s)+@+[A-Z0-9.-]+\.[A-Z]{2,4})'
        email_regex = re.compile(regex_phrase, re.IGNORECASE)

        for email in email_regex.findall(results_text):
            results.append(email)

        return results

    def close(self):
        """Close googlesearch session
        """
        self.google_search_session.close()
