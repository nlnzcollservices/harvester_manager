import subprocess
import os

def get_video(url, storage_location):
	try:
		cwd = os.getcwd()
		if not os.path.exists(storage_location):
			os.makedirs(storage_location)
		os.chdir(storage_location)
		if url.endswith("/"):
			url = url[:-1]
		__, user_name = url.rsplit("/", 1)
		command = ['fblive', url ]
		subprocess.call(command, shell=True)
		os.chdir(cwd)
		return True, storage_location
	except:
		return False, storage_location 