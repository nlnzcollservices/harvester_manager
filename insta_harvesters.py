import subprocess
import os
import configparser
from datetime import datetime as dt
import youtube_dl

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

def get_video(item):
	print("Instagram video")
	
	item.agent_name = agent_name+"_get_video"
	storage_folder = item.storage_folder
	flag=True
	url = item.url
	vidid=url.split("/")[-1]
	if not os.path.exists(storage_folder):
		os.makedirs(storage_folder)
	try:
		ydl = youtube_dl.YoutubeDL({'outtmpl':os.path.join(storage_folder, vidid+'.'+'%(ext)s')})
		ydl.download([url])	
	except Exception as e:
			print(str(e))
			print(vidid)
			with open(os.path.join(storage_folder,'errors_{}.txt'.format(dt.now().strftime('%Y%m%d'))), "a") as f:
				f.write(vidid + "|" + item.id + " " + str(e) )
				f.write("\n")
				flag = False
		

	item.completed = flag

	return item

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
	print(item.id)
	print("Video")
	url = item.url
	storage_location = item.storage_location
	item.agent_name = agent_name+"-get_live"
	print("here")
	try:
		cwd = os.getcwd()
		if not os.path.exists(item.storage_folder):
			os.makedirs(item.storage_folder)
		print("here2")
		os.chdir(item.storage_folder)
		print("here")
		if url.endswith("/"):
			url = url[:-1]
		__, user_name = url.rsplit("/", 1)
		print("here")
		command = ['pyinstalive', "-d", user_name ]
		subprocess.call(command, shell=True)
		os.chdir(cwd)
		item.completed = True
	except Exception as e:
		print(str(e))
		os.chdir(cwd)
		item.completed = False
	return item

def get_account(item):
	print("here3")
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
	storage_location = item.storage_folder
	item.agent_name = agent_name+"-get_account"
	print(storage_location)
	print(item.agent_name)
	try:
		cwd = os.getcwd()
		if not os.path.exists(storage_location):
			os.makedirs(storage_location)
		os.chdir(storage_location)
		if url.endswith("/"):
			url = url[:-1]
		__, user_name = url.rsplit("/", 1)
		command = ["instagram-scraper", user_name, "-u", insta_username, "-p",  insta_password ]
		print(command)
		subprocess.call(command, shell=True)
		os.chdir(cwd)
		item.completed = True
	except Exception as e:
		print(e)
		os.chdir(cwd)
		item.completed = False
	return item
