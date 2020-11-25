from googlesearch import Googlesearch


class Linkedinaddress:
    def __init__(self):
        """Class which outputs company's LinkedIn addresses from Google search.
        """
        self.googlesearch = Googlesearch()

    def _get_search_data(self, search_phrase, pages):
        """Use googlesearch.py for looking for search phrase results. Linkedin keyword is added to the company name passed.

        Args:
            search_phrase (string): The name of the company you are looking for without any additional keywords.
            pages (int, optional): Number of pages to handle. Defaults to 1.

        Returns:
            list: List of dictionaries from googlesearch.py.
        """
        result = self.googlesearch.get_search_results(
            search_phrase + " linkedin")
        return result

    def get_linkedin_address(self, search_phrase, pages=1):
        """Outputs the list of linkedin addresses that appeared in search results.

        Args:
            search_phrase (string): The name of the company you are looking for without any additional keywords.
            pages (int, optional): Number of pages to handle. Defaults to 1.

        Returns:
            List: List of strings of linkedin addresses to linkedin companies.
        """
        result_data = self._get_search_data(search_phrase, pages)
        output_data = []
        for item in result_data["search-result-list"]:
            if "linkedin.com/company/" in item["link"]:
                output_data.append(item["link"])
        return output_data

    def close_googlesearch(self):
        """Close googlesearch object.
        """
        self.googlesearch.close()
