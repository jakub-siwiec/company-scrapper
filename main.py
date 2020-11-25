import pandas as pd
from rocketreach import Rocketreach
from hunter import Hunter
from linkedinsearch import Linkedinsearch
from decouple import config


def email_rocketreach(name):
    search = Rocketreach(name)
    return search.get_results()


def email_hunter(domain_name):
    search = Hunter(domain_name)
    results = search.get_results()
    return [results["email_pattern"], results["email_list"]]


def populate_hunter(df):
    df[["Email Pattern", "Emails"]] = df.apply(
        lambda x: email_hunter(x["Domain"]), axis=1, result_type="expand")
    return df


def hunter_main():
    """Main function to search for emails.
    """
    df = pd.read_excel(config('HUNTER_XLSX_FILE_INPUT'), index_col=0)
    df = populate_hunter(df)
    print(df)
    df.to_excel(config('HUNTER_XLSX_FILE_OUTPUT'))


def people_search_linkedin(linkedin_session_object, company_name):
    """Search phrase on LinkedIn, scrap results and save to csv.

    Args:
        linkedin_session_object (object): Linkeinsearch object.
        company_name (string): Phrase to search in LinkedIn browser.
    """
    linkedin_session_object.search(company_name)
    linkedin_session_object.scrap_and_update_csv()


def linkedin_search_main():
    """Puts Linkedinsearch object, data to go through together and conducts the operation of scrapping profiles from LinkedIn search. It uses the column called Name to get search phrases.
    """
    linkedin_session = Linkedinsearch()
    df = pd.read_excel(config('LINKEDIN_XLSX_FILE_INPUT'), index_col=0)
    df["Name"].apply(lambda name: people_search_linkedin(
        linkedin_session, name))
    linkedin_session.close()


def people_company_linkedin(linkedin_session_object, company_name, linkedin_company_url):
    """Scraps people who are listed on the company's Linkedin site.

    Args:
        linkedin_session_object (object): Linkeinsearch object.
        company_name (string): Company name.
        Full company LinkedIn address of the format https://www.linkedin.com/company/[company-user-name]/.
    """
    linkedin_session_object.company_people_list(
        company_name, linkedin_company_url)
    linkedin_session_object.scrap_and_update_csv()


def linkedin_company_main():
    """Puts Linkedinsearch object, data to go through together and conducts the operation of scrapping profiles from LinkedIn company profiles. It uses the column called Name to get search phrases and Linkedin to get LinkedIn compamy's profile address.
    """
    linkedin_session = Linkedinsearch()
    df = pd.read_excel(config('LINKEDIN_XLSX_FILE_INPUT'), index_col=0)
    df.apply(lambda x: people_company_linkedin(
        linkedin_session, x["Name"], x["Linkedin"]), axis=1)
    linkedin_session.close()
