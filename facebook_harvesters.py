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
		name = name.replace("?", "_").replace("=", "_")
		command = ['fbdown', url]
		subprocess.call(command, shell=True)

		for f in os.listdir(storage_location):
			if not f.endswith(".mp4"):
				src = os.path.join(storage_location, f)
				dst = os.path.join(storage_location, f+".mp4")
				os.rename(src, dst)

		os.chdir(cwd)
		return True
	except:
		os.chdir(cwd)
		return False