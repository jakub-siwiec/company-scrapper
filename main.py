import pandas as pd
from rocketreach import Rocketreach
from hunter import Hunter
from decouple import config


def Email_rocketreach(name):
    search = Rocketreach(name)
    return search.get_results()


def Email_hunter(domain_name):
    search = Hunter(domain_name)
    results = search.get_results()
    return [results["email_pattern"], results["email_list"]]


def Populate_hunter(df):
    df[["Email Pattern", "Emails"]] = df.apply(
        lambda x: Email_hunter(x["Domain"]), axis=1, result_type="expand")
    return df


df = pd.read_excel(config('XLSX_FILE_INPUT'), index_col=0)
df = Populate_hunter(df)
print(df)
df.to_excel(config('XLSX_FILE_OUTPUT'))
