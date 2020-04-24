import subprocess
import os
import configparser

agent_name = "insta_harvesters_1"

config = configparser.ConfigParser()
sprsh_file = r"C:\Source\secrets_and_credentials\spreadsheet"
config.read(sprsh_file)

try:
	insta_username = config.get("configuration","insta_user_name")
	insta_password = config.get("configuration","insta_password")
except configparser.NoOptionError:
	pass



def get_live(item):
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
