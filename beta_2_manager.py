import os
import gspread
import json
import sys
from oauth2client import file
from datetime import datetime as dt
import httplib2
import dateparser
import subprocess
import configparser
from insta_harvesters import get_live as insta_get_live
from insta_harvesters import get_account as insta_get_account
from tiktok_harvesters import get_tiktok_video as tiktok_get_video 
from facebook_harvesters import get_video as facebook_get_video
from youtube_harvesters import get_video as youtube_get_video

# project_folder = "\\".join(os.getcwd().split('\\')[:-1])
sys.path.insert(0, r'C:\Source\secrets_and_credentials')
script_folder = os.getcwd()
secrets_and_credentials_fold = r"C:\Source\secrets_and_credentials"
sprsh_file = os.path.join(secrets_and_credentials_fold, "spreadsheet")
config = configparser.ConfigParser()
config.read(sprsh_file)

## credentials
sprsh = config.get("configuration","sprsh")

try:
	insta_username = config.get("configuration","insta_user_name")
	insta_password = config.get("configuration","insta_password")
except configparser.NoOptionError:
	pass


try: 
	twitter_consumer_key = config.get("configuration","twitter_consumer_key")
	twitter_consumer_secret = config.get("configuration","twitter_consumer_secret")
	twitter_access_token = config.get("configuration","twitter_access_token")
	twitter_access_token_secret = config.get("configuration","twitter_access_token_secret")
except configparser.NoOptionError:
	pass



credential_file = os.path.join(secrets_and_credentials_fold, "credentials")
client_secrets_file = os.path.join(secrets_and_credentials_fold, "client_secrets.json")
store = file.Storage(client_secrets_file )
creds = store.get()
#automatically renews google credentials
if creds.access_token_expired:
	creds.refresh(httplib2.Http())
#authorizing credentials
c = gspread.authorize(creds)
#gets spreadsheet
gs = c.open_by_key(sprsh)
#gets sheet by name
ws = gs.get_worksheet(0)

### make storage folder 
storage_folder_root = "./harvests"
if not os.path.exists(storage_folder_root):
	os.makedirs(storage_folder_root) 

### get local content types
### if you don't have a file in the root folder called 'my_content_types.txt' nothing will process.
### Use 'my_content_types_master.txt' as a refernce
if not os.path.exists('my_content_types.txt'):
	my_content_types = []
else:
	with open('my_content_types.txt') as data:
		my_content_types = [x for x in data.read().split('\n') if x != ""]


class Item():
	def __init__(self, row, row_number):
		self.id = row[0]
		self.description = row[1]
		self.creator = row[2]
		self.ready = row[3]
		self.category = row[4]
		self.location = row[5]
		self.content_type = row[6]
		self.url = row[7]
		self.date_range = dateparser.parse(row[8])
		self.reccuring = row[9]
		self.scope = row[10]
		self.archived = dateparser.parse(row[11])
		self.collected = row[12]
		self.responsible = row[13]
		self.storage_location = row[14]
		self.notes = row[15]
		self.completed = False
		self.storage_folder = os.path.join(storage_folder_root, self.id)
		self.row_number = row_number
		self.agent_name = ""
		self.archived_start_date = ""
		if self.reccuring == "Y":
			if self.archived == None:
				self.archived_start_date = self.date_range
			else:
				self.archived_start_date = self.archived
		if self.reccuring == "N":
			self.archived_start_date = self.date_range



def item_parser(item):

	if item.ready == "Y" and item.collected != "Y":
		if item.content_type == "InstagramAccount" and item.content_type in my_content_types:
			item = insta_get_account(item)
		elif item.content_type == "InstagramLive" and item.content_type in my_content_types:
			item = insta_get_live(item)
		elif item.content_type == "TiktokVideo" and item.content_type in my_content_types:
			item = tiktok_get_video(item)
		elif item.content_type == "FacebookVideo" and item.content_type in my_content_types:
			item = facebook_get_video(item)

		# my_harvester = Youtube_harvester(self.data)
		# elif self.content_type == "InstagramItem" and self.content_type in my_content_types:
		# 		flag, self.location = instagramm_item()
		# elif self.content_type == "VimeoVideo" and self.content_type in my_content_types:
		# 		flag, self.location = vimeo_video()
		# elif self.content_type == "YoutubeVideo" and self.content_type in my_content_types:
		# 		flag, self.location = my_harvester.youtube_video()
		# elif self.content_type == "YoutubChannel" and self.content_type in my_content_types:
		# 		flag, self.location = my_harvester.youtube_channel()
				
		elif item.content_type == "YoutubeUser" and item.content_type in my_content_types:
			item = my_harvester.youtube_user(item)
		#print(self.content_type, self.date_range, self.storage_folder)
		if item.completed:
			write_to_spreadsheet(item)

def write_to_spreadsheet(item):

	"""
	Writes to spreadsheet collect, responsible, storage location

	"""
	ws.update_cell(item.row_number, 11, dt.now().stftime("%d.%m.%Y") )
	ws.update_cell(item.row_number, 13, item.agent_name)
	ws.update_cell(item.row_number, 14, item.storage_location)
	
	if not item.recurring:
		ws.update_cell(self.row_number, 12, "Y")
	else:
		ws.update_cell(self.row_number, 12, "N")

def main():

	"""
	Initiates reading spreadsheet by rows

	"""

	row_count  = ws.row_count
	for row_number, row in enumerate(ws.get_all_values()[1:], start = 2):
		item = Item(row, row_number)
		item_parser(item)

if __name__ == "__main__":
	main()

