import subprocess
import os
import sys
import requests
#import fbdown

# sys.path.insert(0,r'C:\Users\Korotesv\fbdown')
# from fbdown import TheMain as fbdown

agent_name = "facebook_harvesters_1"

def get_video(item):

	"""
	Gets a single video from a given facebook video page URL
	Has 3 steps. 
	1. Attempts to find facebook video ID from given URL, 
	2. Attemps to download that video binary from the video id via the fbdown tool (commandline call)
	https://tbhaxor.github.io/fbdown/
	3. Updates the item() data object
	
	todo
	Resulting data needs to reshaped into standardised format
	URL cleanup could be better
	"""
	try:
		if not 'facebook.com' in item.url:
			r = requests.get(item.url)
			url = r.url
		else:
			url = item.url
		storage_location = item.storage_location
		item.agent_name = agent_name+"_get_video"
		cwd = os.getcwd()
		#item.storage_folder = item.storage_folder.replace("/","\\")
		if not os.path.exists(item.storage_folder):
			os.makedirs(item.storage_folder)
		os.chdir(item.storage_folder)
		item.storage_location = os.getcwd()
		print(item.storage_location)
		if url.endswith("/"):
			url = url[:-1]
		__, user_name = url.rsplit("/", 1)
		print(user_name)
		print("here")
		name = user_name.replace("?", "_").replace("=", "_").replace("?", "_").replace("=","_")
		print(name)
		print(url.split("/")[-1])
		print(url)
		command = ['python',r'C:\Source\fbdown.py', url]
		subprocess.call(command, shell=True)
		#fbdown.main(url, item.storage_location)

		
		for f in os.listdir(item.storage_location):
			if not f.endswith(".mp4"):
				src = os.path.join(item.storage_location, f)
				dst = os.path.join(item.storage_location, f+".mp4")
				os.rename(src, dst)

		os.chdir(cwd)
		item.completed = True
		if os.listdir(item.storage_location)==[]:
			item.completed = False
	except Exception as e:
		print(str(e))
		os.chdir(cwd)
		item.completed = False
	return item
