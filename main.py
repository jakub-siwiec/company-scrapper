import pandas as pd
from rocketreach import Rocketreach
from hunter import Hunter
from linkedinsearch import Linkedinsearch
from linkedinaddress import Linkedinaddress
from decouple import config


def email_rocketreach(name):
    search = Rocketreach(name)
    return search.get_results()


def email_hunter(domain_name):
    search = Hunter(domain_name)
    results = search.get_results()
    return [results["email_pattern"], results["email_list"]]


def _populate_hunter(df):
    df[["Email Pattern", "Emails"]] = df.apply(
        lambda x: email_hunter(x["Domain"]), axis=1, result_type="expand")
    return df


def hunter_main():
    """Main function to search for emails.
    """
    df = pd.read_excel(config('HUNTER_XLSX_FILE_INPUT'), index_col=0)
    df = _populate_hunter(df)
    print(df)
    df.to_excel(config('HUNTER_XLSX_FILE_OUTPUT'))


def _people_search_linkedin(linkedin_session_object, company_name):
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
    df["Name"].apply(lambda name: _people_search_linkedin(
        linkedin_session, name))
    linkedin_session.close()


def _people_company_linkedin(linkedin_session_object, company_name, linkedin_company_url):
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
    df.apply(lambda x: _people_company_linkedin(
        linkedin_session, x["Name"], x["Linkedin"]), axis=1)
    linkedin_session.close()


def _get_linkedin_address(google_session, df_companies):
    """Get Linkedin addresses for the companies from the list. They can require cleaning the data (e.g. because of duplicates for various languages). It has to have column Name with companies' names.

    Args:
        google_session (object): Linkedinaddress object.
        df_companies (dataframe): Pandas DataFrame with the list of companies with their names.

    Returns:
        dataframe: Pandas DataFrame with companies' names and LinkedIn addresses
    """
    df_output = pd.DataFrame(columns=["Name", "Linkedin"])
    for index, row in df_companies.iterrows():
        name = row["Name"]
        linkedin = google_session.get_linkedin_address(row["Name"])
        for address in linkedin:
            df_output = df_output.append(
                {"Name": name, "Linkedin": address}, ignore_index=True)
    return df_output


def search_linkedin_address():
    """Search for LinkedIn addresses for data from Excel spreadsheet. It has to have column Name with companies' names.
    """
    google_session = Linkedinaddress()
    df = pd.read_excel(config('COMPANY_NAME_XLSX_FILE_INPUT'), index_col=0)
    df_output = _get_linkedin_address(google_session, df)
    df_output.to_excel(config('COMPANY_NAME_XLSX_FILE_OUTPUT'))
    google_session.close_googlesearch()
