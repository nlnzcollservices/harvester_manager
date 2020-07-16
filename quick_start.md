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

## Step One - Python. 

Clone the repo on your local mahcine. 
Install / upgrade python as needed to v3.6 minimum. 
install the needed libs in python. From commandline: `pip3 install gspread`, `pip3 install BeautifulSoup4, `pip3 install dateparser`, `pip3 install oauth2client`, 'pip3 install httplib2',  

## Step Two - Google sheet. 

Follow the instuctions by google for setting up new spreadsheet.


???... 


Populate the header row (row #1) with the column headings 

Copy/ paste the next line in cell A1 in your sheet. Select the cell A1 in googledocs, press and hold 'left-alt', then press and release `d`, then press and release `e` - this will open the 'Data' menu, and select the "text to columns" option. Automatic should work fine]:

Unique Identifier, Brief Description, Creator (if known), Ready for harvest (Y/N/?), Category, Location, Content Type (list), Link, Date range, Recurring (Y/N), Scope, Date Archived, Collected (Y/N), Staff/Team Responsible, Storage Location, Notes, Screengrabs (Y/N)	


## Step Three - Secrets File


There is two secrets files needed for this. 
1. from `beta_2_manager.py` 

        sys.path.insert(0, r'C:\Source\secrets_and_credentials')
        script_folder = os.getcwd()
        secrets_and_credentials_fold = r"C:\Source\secrets_and_credentials"
        sprsh_file = os.path.join(secrets_and_credentials_fold, "spreadsheet")
        config = configparser.ConfigParser()
        config.read(sprsh_file)

        ## credentials
        sprsh = config.get("configuration","sprsh")
        
make a text file called "spreadsheet" , in the folder specificed in 'secrets_and_credentials_fold'. You can change either of these to something more suitable, make sure you change the code accordingly. 

2. from `beta_2_manager.py` 

      credential_file = os.path.join(secrets_and_credentials_fold, "credentials")
      client_secrets_file = os.path.join(secrets_and_credentials_fold, "client_secrets.json")

Put the credentials file from step 2 into the same folder, rename it "client_secrets.json".  You can change the name to something more suitable,  make sure you change the code accordingly. 

