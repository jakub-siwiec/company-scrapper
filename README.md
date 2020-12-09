# Company scrapper

A toolset for getting information about companies from Google, LinkedIn, Hunter and then preparing the data to send with email-mass-sender (my another repo).

**Purpose:** Personal, *only educational* purposes. 

## Summary

### Technologies

Languages:

* Python

Web-based automation tool:

* Selenium

Package manager:

* Virtualenv

Additional packages/tools:

* Jupyter Lab
* Pandas
* [ipysheet](https://github.com/QuantStack/ipysheet)
* [extract-emails](https://github.com/dmitriiweb/extract-emails)

Used for cleaning the data apart of Jupyter and Python:

* Microsoft Excel

### Setup

Download Chromedriver and save it in the main directory. There is .env file storing private information for Hunter API and LinkedIn login as well as file input and output title. 

```
// Hunter API key to be obtained from hunter.io website
HUNTER_API_KEY

// .xlsx full file name with the data for Hunter API
HUNTER_XLSX_FILE_INPUT

// .xlsx full file name in which will be saed with the data from Hunter API
HUNTER_XLSX_FILE_OUTPUT

// LinkedIn email for logging in
LINKEDIN_EMAIL

// LinkedIn password for logging in
LINKEDIN_PASSWORD

// .xlsx full file name with the data for LinkedIn scrapping
LINKEDIN_XLSX_FILE_INPUT

// .csv full file name for the output from LinkedIn scrapping
LINKEDIN_CSV_FILE_OUTPUT
```

For Hunter file there should be a column called *Domain* with companies' domain addresses without any prefix (such as www. or https) and slashes in the end. Correct entry would be *google.com*.

For LinkedIn the necessary column is called *Name* where you should put the names of the companies you will search in LinkedIn browser.

### How it works

Before presenting capabilities of the apps, I would like to mention that I didn't create this toolset as an optimal, one app. I was focusing on creating new tools I needed (to educate myself with ;) ). Each tool is a seperate story. Therefore you may find some repeating code across the files at least at this moment. Maybe in the future I will work on it.

**main.py**

Imports files and databases to actually make work with the toolset. Use this file to conduct the operations on databases. Most of the things can be done by one simple function from main.py.

**googlesearch.py**

It is a toolset for Google. For example, it can copy all the search results with titles from selected number of search result pages and return it in the form of dictionary. This file was created after files for hunter, linkedin and rocketreach. However, the purpose of this file is to create googlesearch toolset for other separate functionalities as rocketreach search could be (copying email patterns for companies from Google search results).

**hunter.py**

Uses Hunter API to populate list of the companies with their email patterns and emails that appear in hunter.io database.

**linkedinsearch.py**

Scraps results from LinkedIn. There are two possible options to get the data.

1. You scrap people profiles through LinkedIn search. If you insert the company name in the LinkedIn search you will get the results. Most of them will be people connected with that company. There can be current employees or past employees. This is also a good way to discover similar companies.
2. You know the company's LinkedIn profile address and scrap people's profiles from their LinkedIn site. These are the people who are currently signed to the company.

**linkedinaddress.py**

Searching for LinkedIn addresses using googlesearch.py. You input the name and the app searches for LinkedIn addresses in search results. There can be some duplicates (e.g. different LinkedIn country codes) because I decided to go with all the addresses that appear in the results rather than the first ones, so the data may require cleaning.

**sitecrawler.py**

Gets links which are in the site.

**linkedinwebsite.py**

Gets company's website url from their LinkedIn profile page.

**websitemail.py**

Uses extract-emails for getting email addresses from websites fast crawling in the websites.

**generator.ipynb**

Jupyter Notebook which receives cleaned data (how to clean it is described below) and thanks to functions in tools.jupyterfunctions and ipysheet generates .csv file (with $ as a separator) in a fraction of time comparing to typing and which requires only separating to columns in Excel to have a ready file to send by [email-mass-sender](https://github.com/jakub-siwiec/email-mass-sender).

Saving to excel is made in append mode on purpose. The Jupyter Notebook was created to include there each company separately (in order to check which people are an appropriate choice for addressing an email).

**tools files: outputfilenamegenerator.py, jupyterfunctions.py, public.constants.py, privateconstants.py (invisible, included in .gitignore)**

Files helping with efficiency and cleaningness of the code. You can find a description what is inside privateconstants.py in jupyterfunctions.py.

## How to work with the scrapper

This is a procedure I recommend to apply.

Let's assume you have a long list of companies' names.

1. You look for email format in Google of the companies from the list.

Thanks to that you obtain not only email formats of companies' employees, but also a domain name, which probably will be the same as the website address.

2. You look for LinkedIn sites in Google for all the companies.

This is a gateway for people's list and website addresses of the companies. 

3. You clean the data from the step 1. and 2.

You convert emails formats which you've got in the first step into one universal style (e.g. {first_name}{last_name}@...) so that you would be able to work with the people's names from later steps. I recommend using the style of hunter.io or rocketreach depending on which one you would use to get other email formats. 

More time-consuming procedure is cleaning the data from step 2. Unfortunately, you will get many duplicates and, worse, companies of the same name on LinkedIn. There is no other way to clean the data than just looking at companies profiles and find which one is suitable (unless you have a very strict criteria regarding companies' location and industry).

4. You look for website addresses of the companies on their LinkedIn sites.

Thanks to that you obtain their website addresses and domains.

5. You look for emails on the companies crawling their websites.

Using functions from extract-email you get the emails which appear on company's websites you've got.

6. You get remaining email formats and some emails using Hunter.io

You prepare a separate file for the companies for which you have a domain name in a correct format (no prefix, just suffix, no signs, e.g. github.com). You get the email formats and list of emails (usually such as info@company.com).

7. You clean the files to prepare them for final processiong in Jupyter Notebook.

I personally use Microsoft Excel and Jupyter Notebook for cleaning the data.

You need 2 files: final_company_list.xlsx (organised data about the companies) and final_linked_list.csv (the list of people). Kind of foreign key for these tables (so the value that must be the same to match the records from both of the tables) is company's name. 

These are the requirements for the column names and format:

```
final_company_list.xlsx

- Name 

Company's name.

- Domain 

Company's domain, no prefix, just suffix, e.g. azure.com.

- EmailPattern 

Email pattern in the format {first}.{last}@company.com or {f}{last}@company.com where {first} and {last} are full first and last names and {f} and {l} are first letters of first and last names. 

If there are several email patterns they should be separated by the comma and space e.g. {first}{l}@company.com, {last}@company.com.

- EmailList

List of additional email addresses which could potentially be email receipients. If there are some more they should be separated with comma and space. E.g. info@company.com, contact@company.com.



final_linked_list.csv

Comma separated file with $ as a separator.

- Name 

The person full name.

- Company

Company's name.

- Description

LinkedIn description, e.g. Project Manager at Amazon.

- Location

Person location from LinkedIn. Used for information purposes. Not obligatory but very useful.

- Link

LinkedIn link to the person used only for information purposes. Not obligatory but very useful.

```

8. Working on data in Jupyter Notebook returning the file to use by email-mass-sender

Thanks to ipysheet and some functions the work should go very fast. In this file we choose a company (one by one), choose extra email addresses to send emails to (such as info@company.com). Then we get a list of people from final_linked_list from that company. We choose these we are interested in. The app generates correct email format(s), templates for email-mass-sender. We have a possibility to correct potential mistakes (quickly, ipysheet works like a spreadsheet editor similar to Excel but in Jupyter). When everything is correct, the next step is appending generated data to tosend.csv file.

9. Final preparation for email mass sending with email-mass-sender

Copying, pasting and separating text to columns. The data is ready.

## Final notes

This app could also be edited and used for many business purposes, however it's built only for education purposes. You bear the responsibility for how you use it.