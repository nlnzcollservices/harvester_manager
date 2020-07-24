import urllib.request
import requests
from bs4 import BeautifulSoup as bs
import os

session = requests.Session()
session.headers.update({'User-Agent': 'Custom user agent'})

agent_name = "tiktok_harvesters_1"

def get_tiktok_video(item):
	"""
	Gets a single video from a given facebook video page URL
	Has 3 steps. 
	1. Attempts to find facebook video ID from given URL, 
	2. Attemps to download that video binary from the video id via python
	https://tbhaxor.github.io/fbdown/
	3. Updates the item() data object
	
	todo
	Resulting data needs to reshaped into standardised format
	URL cleanup could be better
	"""
	
	url = item.url
	storage_location = item.storage_location
	item.agent_name = agent_name+"_get_video"
	cwd = os.getcwd()
	if not os.path.exists(storage_location):
		os.makedirs(storage_location)
	os.chdir(storage_location)
	if url.endswith("/"):
		url = url[:-1]
	__, name = url.rsplit("/", 1)
	name = name+".mp4"
	parent = bs(session.get(url).text, features="html5lib") 
	urllib.request.urlretrieve(parent.find("video")["src"], name)
	os.chdir(cwd)
	item.completed = True
	return item
