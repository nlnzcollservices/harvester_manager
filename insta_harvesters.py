import subprocess
import os

def get_live(url, storage_location):
	cwd = os.getcwd()
	if not os.path.exists(storage_location):
		os.makadirs(storage_location)
	os.chdir(storage_location)
	if url.endswith("/"):
		url = url[:-1]
	__, user_name = url.rsplit("/", 1)
	command = ['pyinstalive', "-d", user_name ]
	subprocess.call(command, shell=True)
	os.chdir(cwd)
	return True, storage_location


def get_account(url, storage_location):
	cwd = os.getcwd()
	if not os.path.exists(storage_location):
		os.makedirs(storage_location)
	os.chdir(storage_location)
	if url.endswith("/"):
		url = url[:-1]
	__, user_name = url.rsplit("/", 1)
	command = ["instagram-scraper", user_name, "-u", insta_username, "-p",  insta_password ]
	subprocess.call(command, shell=True)
	# instagram-scraper lizstokedstokes -u  nlnz_harvester -p Y,yQ3_Y_R7Smm)+
	os.chdir(cwd)
	return True, storage_location

url = "https://www.instagram.com/jaygattuso/"
insta_username = "nlnz_harvester"
insta_password = "Y,yQ3_Y_R7Smm)+"

storage_location =  r"C:\projects\misc_harvesters\manager\harvests\junk"
get_account(url, storage_location)


