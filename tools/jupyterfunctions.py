import pandas as pd
import numpy as np
import ipysheet
from .publicconstants import FIXES_TO_DELETE
from .privateconstants import OUTPUT_COLUMN_LIST, EMAIL_TEMPLATE_HR, EMAIL_TEMPLATE_VARIABLES

# private constants:
# OUTPUT_COLUMN_LIST - the list of names of the columns in the final output
# EMAIL_TEMPLATE_HR - the dictionary of options of template variables which change depending on whether the email will be sent to HR or not
# EMAIL_TEMPLATE_VARIABLES - the dictionary for template variables in the emails with the correct keys for these templates used in email-mass-sender


def get_private_dictionary(private_dictionary, index):
    """Get value from the dictionary by index. Used for dictionaries in privateconstants.py.

    Args:
        private_dictionary (dictionary): Private dictionary to process.
        index (int): Number of the index.

    Returns:
        dictionary: Dictionary with the keys "key" and "value".
    """
    return {"key": list(private_dictionary)[index], "value": private_dictionary[list(private_dictionary)[index]]}


def create_ipysheet_from_df(df, height="1000px", width="960px"):
    """Create ipysheet from Pandas DataFrame with custom settings.

    Args:
        df (DataFrame): Pandas DataFrame to convert.
        height (str, optional): Value for the height of the sheet. Defaults to "1000px".
        width (str, optional): Value for the width of the sheet. Defaults to "960px".

    Returns:
        ipysheet sheet: Converted ipysheet sheet.
    """
    sheet = ipysheet.pandas_loader.from_dataframe(df)
    sheet.layout.height = height
    sheet.layout.width = width
    return sheet


def get_checkbox_true(ipy_sheet):
    """Get DataFrame with the rows where checkbox was set to True from the ipysheet sheet.

    Args:
        ipy_sheet (ipysheet sheet): Ipysheet sheet with the column called "Checkbox" with the checkbox.

    Returns:
        DataFrame: Pandas DataFrame with the rows where the checkbox was set to True (ticked).
    """
    df_temp = ipysheet.pandas_loader.to_dataframe(ipy_sheet)
    return df_temp[df_temp["Checkbox"] == True]


def get_names_with_checkbox_true(ipy_sheet):
    """Get list of the values from the column called "Name" with checkbox in the column called "Checkbox" set to True (ticked).

    Args:
        ipy_sheet (ipysheet sheet): Ipysheet sheet with the column called "Checkbox" with the checkbox and "Name" to output.

    Returns:
        list: List of values from the column "Name" with checkboxes set to True (ticked).
    """
    return get_checkbox_true(ipy_sheet)["Name"].tolist()


def get_full_list_people_from_company(df_full_people, companies_list, height="1000px", width="960px"):
    """Get an ipysheet of the people from specific companies.

    Args:
        df_full_people (DataFrame): pandas DataFrame containing the full list of people with companies assigned. They should have a column called "Company".
        companies_list (list): Names of the companies to lookup within df_full_people DataFrame.
        height (str, optional): Value for the height of the sheet. Defaults to "1000px".
        width (str, optional): Value for the width of the sheet. Defaults to "960px".

    Returns:
        ipysheet sheet: Sheet with the peoples data. If empty then returns empty DataFrame with column names.
    """
    df_people_company = df_full_people[df_full_people["Company"].isin(
        companies_list)]
    df_people_company.reset_index(drop=True, inplace=True)
    df_people_company.insert(0, "Checkbox", False)
    if len(df_people_company.index) > 0:
        return create_ipysheet_from_df(df_people_company, height, width)
    else:
        return df_people_company


def get_company_email_data_string(df_single_company):
    """Returns an output to print (use the function print with it) of one specific company into readable string.

    Args:
        df_single_company (DataFrame): DataFrame with 1 item.

    Returns:
        string: Text with information
    """
    try:
        space = " "
        space_line = " - "
        next_paragraph = "\n\n"
        main_title = "Company: "
        company_name = df_single_company.reset_index(
            drop=True).at[0, "Name"]
        company_domain = df_single_company.reset_index(
            drop=True).at[0, "Domain"]
        company_website = df_single_company.reset_index(
            drop=True).at[0, "Website"]
        first_title_string = "Email patterns:\n\n"
        first_results_string = df_single_company.reset_index(
            drop=True).at[0, "EmailPattern"]
        second_title_string = "\n\nEmail list:\n\n"
        second_results_string = df_single_company.reset_index(
            drop=True).at[0, "EmailList"]
        return main_title + company_name + space_line + company_domain + space + company_website + next_paragraph + first_title_string + first_results_string + second_title_string + second_results_string
    except:
        return ""


def extra_impersonal_emails_to_check(df_single_company):
    """Creating ipysheet sheet from the string of extra emails, which should be separated by comma and space ", ".

    Args:
        df_single_company (DataFrame): DataFrame with 1 item.

    Returns:
        ipysheet sheet: ipysheet sheet with checkboxes next to emails. If error then returns None
    """
    try:
        df_additional_info = pd.DataFrame({"Checkbox": False, "Email": df_single_company.reset_index(
            drop=True).at[0, "EmailList"].split(", ")})
        return create_ipysheet_from_df(df_additional_info, height="150px", width="960px")
    except:
        return None


def final_dataframe_with_impersonal_emails(sheet_checked_impersonal_emails, df_single_company):
    """It converts ipysheet sheet with checkboxes set to True (ticked) and make from it a DataFrame ready to save to excel file with all the needed columns.

    Args:
        sheet_checked_impersonal_emails (ipysheet sheet): Sheet with checkboxes set to True for emails to include.
        df_single_company (DataFrame): DataFrame with 1 item.

    Returns:
        DataFrame: Pandas DataFrame ready to send filled with correct values for impersonal emails.
    """
    df_output = pd.DataFrame(columns=OUTPUT_COLUMN_LIST)
    try:
        df_chosen_emails = get_checkbox_true(sheet_checked_impersonal_emails)
        email_list = df_chosen_emails["Email"].tolist()
        for email in email_list:
            df_output = df_output.append(add_impersonal_email(
                df_single_company, email, df_single_company.reset_index(drop=True).at[0, "Name"]))
        return df_output
    except:
        return df_output


def get_name(full_name):
    """Gets first and last name from full name.

    Args:
        full_name (string): Full name of the person.

    Returns:
        list: List of strings where first name is the first item in the list and last name is the last one.
    """
    parts_to_delete = FIXES_TO_DELETE

    for part in parts_to_delete:
        full_name = full_name.replace(part, "")
    names_array = full_name.split(" ", 1)
    names_array[0] = names_array[0].title()
    names_array[1] = names_array[1].title()
    return names_array


def get_position(description):
    """Gets the position from the string if there is a standard LinkedIn position description pattern.

    Args:
        description (string): Full LinkedIn profession description.

    Returns:
        string: The name of the position.
    """
    return description.split(" at ")[0]


def get_domain(df_company_data):
    """Get domain name from DataFrame where the column name is a Domain and there is just one item. Used for the DataFrame of the selected company.

    Args:
        df_company_data (DataFrame): DataFrame with 1 item.

    Returns:
        string: Domain name.
    """
    return df_company_data.reset_index(drop=True).at[0, "Domain"]


def get_email(df_company_data, first_name, last_name, domain):
    """Generating email address from 

    Args:
        df_company_data (DataFrame): DataFrame with 1 item.
        first_name (string): First name.
        last_name (string): Last name.
        domain (string): Domain name with suffix but no prefix.

    Returns:
        list: List of email addresses.
    """
    email_address = []
    email_patterns = df_company_data.reset_index(
        drop=True).at[0, "EmailPattern"]

    first_name = first_name.replace("'", "")
    last_name = last_name.replace("'", "")

    if email_patterns != email_patterns or email_patterns == "nan" or email_patterns == np.nan or email_patterns == "":
        email_address.append(
            (str(first_name) + "." + str(last_name) + "@" + str(domain)).replace(" ", "").lower())
        email_address.append(
            (str(first_name) + str(last_name) + "@" + str(domain)).replace(" ", "").lower())
        email_address.append(
            (str(first_name[0]) + str(last_name) + "@" + str(domain)).replace(" ", "").lower())
        email_address.append(
            (str(first_name) + "@" + str(domain)).replace(" ", "").lower())
    else:
        email_patterns_list = email_patterns.split(", ")
        for index, email_pattern in enumerate(email_patterns_list):
            email_address.append(email_pattern)
            email_address[index] = email_address[index].replace(
                "{f}", first_name[0])
            email_address[index] = email_address[index].replace(
                "{first}", first_name)
            email_address[index] = email_address[index].replace(
                "{l}", last_name[0])
            email_address[index] = email_address[index].replace(
                "{last}", last_name)
            email_address[index] = email_address[index].replace(
                " ", "").lower()

    # Special for names with - such as
    for index, email in enumerate(email_address):
        if "-" in email.split("@")[0]:
            email_address = email_address[:index] + [str(email.split(
                "@")[0].replace("-", "") + "@" + email.split("@")[1])] + email_address[index:]

    return email_address


def hr_finder(position):
    """Detects possible person from HR (can be used for adjusting the message to that person).

    Args:
        position (string): Position description.

    Returns:
        string: Adjusted string. If yes, then it's for HR and if no then for other people.
    """
    keywords_list = ["hr", "human resources", "recruitment",
                     "recruiter", "recruiting", "talent", "office "]

    for keyword in keywords_list:
        if keyword in str(position).lower():
            return EMAIL_TEMPLATE_HR["yes"]

    return EMAIL_TEMPLATE_HR["no"]


def add_impersonal_email(df_company_data, email_address, company):
    """Creating an impersonal a prospective template for impersonal email (with 0 in personal email and no first name and last name).

    Args:
        df_company_data (DataFrame): DataFrame with 1 item.
        email_address (string): Email address to send an impersonal email.
        company (string): Name of the company.

    Returns:
        DataFrame: DataFrame with impersonal email in the correct format to append to the rest of the data.
    """
    df_output_impersonal_email = pd.DataFrame(columns=OUTPUT_COLUMN_LIST)

    temp = {
        "personal": 0,
        "first_name": "",
        "last_name": "",
        "position": "",
        "company": company,
        "email_address": email_address,
        "domain": get_domain(df_company_data),
        get_private_dictionary(EMAIL_TEMPLATE_VARIABLES, 0)["key"]: get_private_dictionary(EMAIL_TEMPLATE_VARIABLES, 0)["value"],
        get_private_dictionary(EMAIL_TEMPLATE_VARIABLES, 1)["key"]: get_private_dictionary(EMAIL_TEMPLATE_VARIABLES, 1)["value"],
        get_private_dictionary(EMAIL_TEMPLATE_VARIABLES, 2)["key"]: get_private_dictionary(EMAIL_TEMPLATE_VARIABLES, 2)["value"],
        get_private_dictionary(EMAIL_TEMPLATE_VARIABLES, 3)["key"]: get_private_dictionary(EMAIL_TEMPLATE_VARIABLES, 3)["value"],
        get_private_dictionary(EMAIL_TEMPLATE_VARIABLES, 4)[
            "key"]: get_private_dictionary(EMAIL_TEMPLATE_VARIABLES, 4)["value"]
    }

    df_output_impersonal_email = df_output_impersonal_email.append(
        temp, ignore_index=True)

    return df_output_impersonal_email


def person_output(person_row, df_company_data):
    """Creating a personal prospective template to send emails for a person.

    Args:
        person_row (series): Pandas series with a person data that will consist of full name, LinkedIn full description and company as well as data from a company's DataFrame with company's name, email format. Adjusts message to HR departments as well.
        df_company_data (DataFrame): DataFrame with 1 item.

    Returns:
        DataFrame: DataFrame in the format ready to save to .csv file.
    """
    df_output_person = pd.DataFrame(columns=OUTPUT_COLUMN_LIST)

    name = get_name(person_row["Name"])
    first_name = name[0]
    last_name = name[1]
    position = get_position(person_row["Description"])
    company = person_row["Company"]
    domain = get_domain(df_company_data)
    email_address = get_email(
        df_company_data, first_name, last_name, domain)
    assist_string = hr_finder(position)

    for email in email_address:
        temp = {
            "personal": 1,
            "first_name": first_name,
            "last_name": last_name,
            "position": position,
            "company": company,
            "email_address": email,
            "domain": domain,
            get_private_dictionary(EMAIL_TEMPLATE_VARIABLES, 0)["key"]: get_private_dictionary(EMAIL_TEMPLATE_VARIABLES, 0)["value"],
            get_private_dictionary(EMAIL_TEMPLATE_VARIABLES, 1)["key"]: get_private_dictionary(EMAIL_TEMPLATE_VARIABLES, 1)["value"],
            get_private_dictionary(EMAIL_TEMPLATE_VARIABLES, 2)["key"]: get_private_dictionary(EMAIL_TEMPLATE_VARIABLES, 2)["value"],
            get_private_dictionary(EMAIL_TEMPLATE_VARIABLES, 3)["key"]: get_private_dictionary(EMAIL_TEMPLATE_VARIABLES, 3)["value"],
            get_private_dictionary(EMAIL_TEMPLATE_VARIABLES, 4)[
                "key"]: assist_string
        }

        df_output_person = df_output_person.append(temp, ignore_index=True)

    return df_output_person


def get_final_people_dataframe(df_checked, df_company):
    """Gets a dataframe with chosen people (by checkbox) and converts it to DataFrame with necessary information for email sending (e.g. email generation, template variable assignment).

    Args:
        df_checked (DataFrame): Pandas DataFrame of people whom we want to include in the list.
        df_company (DataFrame): Pandas DataFrame of companies data to use for people.

    Returns:
        DataFrame: New DataFrame with relevant information
    """
    df_output = pd.DataFrame(columns=OUTPUT_COLUMN_LIST)
    for index, row in df_checked.iterrows():
        df_output = df_output.append(person_output(row, df_company))
    return df_output.reset_index(drop=True)


def get_final_sheet(sheet_people_checked, df_company, height="300px", width="960px"):
    """Generates a final sheet for implementation of final corrections from the sheet with checked checkboxes.

    Args:
        sheet_people_checked (ipysheet sheet): Full ipysheet with filled checkboxes for item we choose.
        df_company (DataFrame): Pandas DataFrame of companies data to use for people.
        height (str, optional): Value for the height of the sheet. Defaults to "300px".
        width (str, optional): Value for the width of the sheet. Defaults to "960px".

    Returns:
        ipysheet sheet: ipysheet with data for final edits. If error (or empty sheet) returns Pandas DataFrame with output column list.
    """
    try:
        df_chosen_people = get_checkbox_true(sheet_people_checked)
        df_final = get_final_people_dataframe(df_chosen_people, df_company)
        sheet_final = create_ipysheet_from_df(
            df_final, height=height, width=width)
        return sheet_final
    except:
        return pd.DataFrame(columns=OUTPUT_COLUMN_LIST)


def get_dataframe_to_save(sheet_people_checked_list, df_additional_impersonal_emails):
    """Output is a final DataFrame which will be saved.

    Args:
        sheet_people_checked_list (ipysheet sheet): sheet_people_checked (ipysheet sheet): Full ipysheet with filled checkboxes for item we choose.
        df_additional_impersonal_emails (DataFrame): Pandas DataFrame with impersonal emails which will be merged with personal DataFrame.

    Returns:
        DataFrame: Final DataFrame to save in Excel.
    """
    try:
        df_output = df_additional_impersonal_emails.append(
            ipysheet.pandas_loader.to_dataframe(sheet_people_checked_list))
        return df_output.reset_index(drop=True)
    except:
        try:
            return df_additional_impersonal_emails
        except:
            return pd.DataFrame(columns=OUTPUT_COLUMN_LIST)


def save_final_df_to_csv(df_final, filename="tosend.csv", sep="$", mode="a"):
    """Save final dataframe to csv file with custom settings.

    Args:
        df_final (DataFrame): Pandas DataFrame with final data we want to save into .csv file. 
        filename (str, optional): The name of csv. Defaults to "tosend.csv".
        sep (str, optional): Seperator in csv file. Defaults to "$".
        mode (str, optional): Mode of save. Defaults to "a" which append the data to the file.

    Returns:
        boolean: True if saved, False if there is an error.
    """
    try:
        df_final.to_csv(filename, sep=sep, mode=mode,
                        index=False, header=False)
        return True
    except:
        return False
