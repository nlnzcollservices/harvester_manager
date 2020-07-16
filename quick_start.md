# Quick start. 

Note 1. It isn't really a quick process to get set up. 

This will out line the parts you need to get going. 

Manditory:
1. A googledocs spreadsheet, and associated credentials. 
2. Python 3.6+
3. A 'secrets' file somewhere on your local machine. 
4. The contents of this git repo.

Depending on the harvesters you need to run, you might need:

1. Access to commandline on your local machine. 
2. Various installers - specified below. 
3. Various username/passwords for platforms - specified below

## Step One. 

Clone the repo on your local mahcine. 
Install / upgrade python as needed to v3.6 minimum. 
install the needed libs in python. From commandline: `pip3 install gspread`, `pip3 install BeautifulSoup4, `pip3 install dateparser`, `pip3 install oauth2client`, 'pip3 install httplib2',  

## Step Two. 

Set up a googledocs sheet: https://docs.google.com/spreadsheets/u/0/ 

Choose new blank sheet. 
Populate the Header row (row #1) with the column headings [copy/ paste the next line]:

Unique Identifier	Brief Description	Creator (if known)	Ready for harvest (Y/N/?)	Category	Location	Content Type (list)	Link	Date range	Recurring (Y/N) 	Scope	Date Archived	Collected (Y/N)	Staff/Team Responsible	Storage Location	Notes	Screengrabs (Y/N)																

## 
