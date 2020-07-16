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

NB. If you plan on running more than one harvester machine, you only need to do this step once. The resulting json file can be shared between all harvesting machines. 

## Step Three - Secrets File


There is two secrets files needed for this. 
1. from `beta_2_manager.py` 

        secrets_and_credentials_fold = r"C:\Source\secrets_and_credentials"
        sprsh_file = os.path.join(secrets_and_credentials_fold, "spreadsheet")
    
        
make a text file called "spreadsheet" , in the folder specificed in 'secrets_and_credentials_fold'. You can change either of these to something more suitable, make sure you change the code accordingly. 

2. from `beta_2_manager.py` 

       credential_file = os.path.join(secrets_and_credentials_fold, "credentials")
       client_secrets_file = os.path.join(secrets_and_credentials_fold, "client_secrets.json")

Put the credentials file from step 2 into the same folder, rename it "client_secrets.json".  You can change the name to something more suitable,  make sure you change the code accordingly. 


## Step Four - Storage

You'll need access to storage - possibly lots. 

Set your root storage location on this line:

        storage_folder_root = "./harvests"

Without changing anything, this line sets the storage location to a subfolder called "harvests" inside whereever the main script is run from. If you want it somehwere else, replace `"./harvests"` with your storage mount point, e.g.  storage_folder_root = `"d:\my_large_hdd\harvests"`

## Step Five - Local content types. 

Each instance can be configured to harvest a subset of the possible content types. This helpful if you have more than one technical stafff working on the harvest, or if you want to isolate specific content types to one machine etc. 

Each harvester needs to have a copy of `my_content_types.txt` which is included in the repo. Open this file on your local machine, and edit the contents, one line per content type, to suit your setup. If you want all the harvests on one machine, open `my_content_types_master.txt` and copy the contents to `my_content_types.txt`
 
## Optional Step Six - fbdown - Needed for facebook live video

From https://tbhaxor.github.io/fbdown/

1. Open cmd with administrator privileges
2. Add pip3 in enviroment variable
3. execute, pip3 install fb-down

Also from https://tbhaxor.github.io/fbdown/ - Get Video Link

1. right click on FB Video
2. left click on Show Video URL
3. copy that URL

This is how to find url of a video to put in the spreadsheet. 

## Optional Step Seven - PyInstaLive - needed for instagram live video

https://github.com/dvingerh/PyInstaLive

You will need an instagram accountname and password. 

from commandline:

`pip3 install pyinstalive`

see the section "Usage" on the github page https://github.com/dvingerh/PyInstaLive to ensure you have the right configuration file `pyinstalive.ini`. 


## Optional Step Eight - Instagram-scraper - needed for instagram accounts

You will need an instagram accountname and password.

Store these in your local secrets file as `insta_user_name` and `insta_password` in the `section` section. Make sure you change the path in `insta_harvesters.py` to match your secrets file location. 


from commandline: 

`pip3 install instagram-scraper`

https://github.com/rarcega/instagram-scraper

## Optional Step Nine - youtube-dl -  needed for Youtube and Vimeo

https://github.com/ytdl-org/youtube-dl/blob/master/README.md#readme

From commandline:

`pip3 install youtube-dl`

## Optional Step Ten - Twarc -  needed for Twitter

https://github.com/DocNow/twarc

Follow the install instructions carefully to set it up. When its installed properly, it manages it own keys. 

