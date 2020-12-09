import pandas as pd
from hunter import Hunter
from linkedinsearch import Linkedinsearch
from linkedinaddress import Linkedinaddress
from linkedinwebsite import Linkedinwebsite
from googlemail import Googlemail
from websitemail import get_website_emails
from tools.outputfilenamegenerator import generate_name
from decouple import config


def email_hunter(domain_name):
    """Get email pattern and email list from hunter.io using their API.

    Args:
        domain_name (string): Domain name without prefix,, but with suffix. No signs such as "/".

    Returns:
        list: List of lists, the first item is email pattern list, the second item is email list that appeared in the search.
    """
    search = Hunter(domain_name)
    results = search.get_results()
    return [results["email_pattern"], results["email_list"]]


def _populate_hunter(df):
    """Takes a DataFrame and adds two additional columns with results from Hunter.io (email pattern and email list).

    Args:
        df (DataFrame): DataFrame with the list of companies and the column called "Domain" with domains.

    Returns:
        DataFrame: Pandas DataFrame with the column with the results.
    """
    df[["Email Pattern", "Emails"]] = df.apply(
        lambda x: email_hunter(x["Domain"]), axis=1, result_type="expand")
    return df


def hunter_main():
    """Main function to search for emails.
    """
    df = pd.read_excel(config('HUNTER_XLSX_FILE_INPUT'), index_col=0)
    df = _populate_hunter(df)
    print(df)
    df.to_excel(generate_name(config('HUNTER_XLSX_FILE_OUTPUT')))


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
    df = pd.read_excel(config('COMPANY_NAME_XLSX_FILE_INPUT'),
                       index_col=None, header=0)
    df_output = _get_linkedin_address(google_session, df)
    df_output.to_excel(generate_name(config('COMPANY_NAME_XLSX_FILE_OUTPUT')))
    google_session.close_googlesearch()


def _get_website_link_from_linkedin(linkedin_session, linkedin_address):
    """Gets website link from LinkedIn company page.

    Args:
        linkedin_session (Linkedinwebsite object): Linkedinwebsite object with an open session in selenium.
        linkedin_address (string): Url address of LinkedIn website of the company.

    Returns:
        string: Company's website link. If didn't find then returns None.
    """
    if linkedin_address == linkedin_address and isinstance(linkedin_address, str):
        try:
            return linkedin_session.get_website_link(linkedin_address)
        except:
            return None
    else:
        return None


def search_website_on_linkedin():
    """Search for website addresses of the companies from Excel file with LinkedIn address (in "Linkedin" column). Returns the results to the file.
    """
    linkedin_session = Linkedinwebsite()
    df = pd.read_excel(config('COMPANY_NAME_LINKEDIN_XLSX_FILE_INPUT'),
                       index_col=None, header=0)
    df["Website"] = df.apply(lambda address: _get_website_link_from_linkedin(linkedin_session, address["Linkedin"]),
                             axis=1)
    df.to_excel(generate_name(
        config('COMPANY_NAME_LINKEDIN_XLSX_FILE_OUTPUT')))
    linkedin_session.close()


def _emails_retriever(google_session, name):
    """Retrieves emails from the results of a specific query in Google.

    Args:
        google_session (Googlemail object): Google session in selenium.
        name (string): Query (company) to search. Additional keywords will be added to the search to increase the efficiency.

    Returns:
        list: List of results or empty string.
    """
    results = google_session.find_emails(name)
    if len(results) > 0:
        print(results)
        return results
    else:
        return ""


def get_emails_from_google():
    """Get emails from Google search
    """
    google_session = Googlemail()
    df = pd.read_excel(config('COMPANY_NAME_GOOGLE_EMAIL_XLSX_FILE_INPUT'),
                       index_col=None, header=0)
    df["Email"] = df.apply(lambda table: _emails_retriever(
        google_session, table["Name"]), axis=1)
    df.to_excel(generate_name(
        config('COMPANY_NAME_GOOGLE_EMAIL_FILE_OUTPUT')))
    google_session.close()


def get_emails_from_websites():
    """Get emails from website using extract_emails package
    """
    df = pd.read_excel(config('COMPANY_NAME_WEBSITE_EMAIL_XLSX_FILE_INPUT'),
                       index_col=None, header=0)
    df["EmailWeb"] = df.apply(
        lambda table: get_website_emails(table["Website"]), axis=1)
    df.to_excel(generate_name(
        config('COMPANY_NAME_WEBSITE_EMAIL_FILE_OUTPUT')))
