import subprocess
import os

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
		url = item.url
		storage_location = item.storage_location
		item.agent_name = agent_name+"_get_video"
		cwd = os.getcwd()
		if not os.path.exists(item.storage_location):
			os.makedirs(item.storage_location)
		os.chdir(item.storage_location)
		if url.endswith("/"):
			url = url[:-1]
		__, user_name = url.rsplit("/", 1)
		name = name.replace("?", "_").replace("=", "_")
		command = ['fbdown', url]
		subprocess.call(command, shell=True)

		for f in os.listdir(storage_location):
			if not f.endswith(".mp4"):
				src = os.path.join(storage_location, f)
				dst = os.path.join(storage_location, f+".mp4")
				os.rename(src, dst)

		os.chdir(cwd)
		item.completed = True
	except:
		os.chdir(cwd)
		item.completed = False
	return item
