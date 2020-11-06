import pandas as pd
from decouple import config
import requests
import json


class Hunter:
    def __init__(self, search_company_domain):
        """Obtain data from hunter.io server through their API

        Args:
            search_company_domain (string): Domain name without any slashes
        """
        self.hunter_api_key = config('HUNTER_API_KEY')
        self.hunter_path = "https://api.hunter.io/v2/domain-search?domain={}&api_key={}".format(
            search_company_domain, config('HUNTER_API_KEY'))
        self.res = requests.get(self.hunter_path)
        self.res_json = self.res.json()

    def get_results(self):
        """Print results of a single search for the company

        Returns:
            dict: Dictionary with email pattern and list of addresses for a certain domain
        """
        result = {
            "email_pattern": str(self.res_json["data"]["pattern"]) + "@" + str(self.res_json["data"]["domain"]),
            "email_list": ", ".join([item["value"] for item in self.res_json["data"]["emails"]])
        }

        return result
