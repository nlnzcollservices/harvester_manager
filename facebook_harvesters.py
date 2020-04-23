import subprocess
import os

agent_name = "facebook_harvesters_1"

def get_video(item):
	try:
		url = item.url
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

		for f in os.listdir(item.storage_location):
			if not f.endswith(".mp4"):
				src = os.path.join(item.storage_location, f)
				dst = os.path.join(item.storage_location, f+".mp4")
				os.rename(src, dst)

		os.chdir(cwd)
		item.completed = True
	except:
		os.chdir(cwd)
		item.completed = False
	return item