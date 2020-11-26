# Company scrapper

A toolset for getting information about companies from Google, LinkedIn, Hunter.

**Purpose:** Personal, *only educational* purposes. 

## Summary

### Technologies

Languages:

* Python

Web-based automation tool:

* Selenium

Package manager:

* Virtualenv

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

Imports files and databases to actually make work with the toolset.

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

**rocketreach.py**

Scraps rocketreach email patterns from Google search results.