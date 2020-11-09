import pandas as pd
from rocketreach import Rocketreach
from hunter import Hunter
from linkedin import Linkedin
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


def people_linkedin(linkedin_session_object, company_name):
    linkedin_session_object.search(company_name)
    linkedin_session_object.scrap()


def linkedin_main():
    linkedin_session = Linkedin()
    df = pd.read_excel(config('LINKEDIN_XLSX_FILE_INPUT'), index_col=0)
    df["Name"].apply(lambda name: people_linkedin(linkedin_session, name))
    linkedin_session.close()
