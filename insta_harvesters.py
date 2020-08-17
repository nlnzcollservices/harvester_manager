import subprocess
import os
import configparser

agent_name = "insta_harvesters_1"

secrets_and_credentials_fold = 'C:\Source\sercrets_and_credentials'
script_folder = os.getcwd()
config = configparser.ConfigParser()
config.read(os.path.join(secrets_and_credentials_fold,"secret"))

try:
	insta_username = config.get("social_media_harvester","insta_user_name")
	insta_password = config.get("social_media_harvester","insta_password")

except configparser.NoOptionError:
	pass



def get_live(item):
	"""
	Gets any instagram "live" video from a given instagram account name
	Has 2 steps: 
	1. Attemps to download video binary from the account name via the pyinstalive (commandline call)
	https://github.com/tinymoss/PyInstaLive
	2. Updates the item() data object
	
	todo
	Resulting data needs to reshaped into standardised format
	"""
	url = item.url
	storage_location = item.storage_location
	item.agent_name = agent_name+"-get_live"
	try:
		cwd = os.getcwd()
		if not os.path.exists(storage_location):
			os.makedirs(storage_location)
		os.chdir(storage_location)
		if url.endswith("/"):
			url = url[:-1]
		__, user_name = url.rsplit("/", 1)
		command = ['pyinstalive', "-d", user_name ]
		subprocess.call(command, shell=True)
		os.chdir(cwd)
		item.completed = True
	except:
		os.chdir(cwd)
		item.completed = False
	return item

def get_account(item):
	"""
	Gets any instagram account from a given instagram account name
	Has 2 steps: 
	1. Attemps to download video binary from the account name via the instagram-scraper tool (commandline call)
	https://github.com/arc298/instagram-scraper
	2. Updates the item() data object
	
	todo
	Resulting data needs to reshaped into standardised format
	Get captions / comments - See work in progress folder in this git
	Do date range filtering
	"""
	
	url = item.url
	storage_location = item.storage_location
	item.agent_name = agent_name+"-get_account"
	try:
		cwd = os.getcwd()
		if not os.path.exists(storage_location):
			os.makedirs(storage_location)
		os.chdir(storage_location)
		if url.endswith("/"):
			url = url[:-1]
		__, user_name = url.rsplit("/", 1)
		command = ["instagram-scraper", user_name, "-u", insta_username, "-p",  insta_password ]
		subprocess.call(command, shell=True)
		os.chdir(cwd)
		item.completed = True
	except:
		os.chdir(cwd)
		item.completed = False
	return item
