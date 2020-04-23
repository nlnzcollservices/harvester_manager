import urllib.request
import requests
from bs4 import BeautifulSoup as bs
import os

session = requests.Session()
session.headers.update({'User-Agent': 'Custom user agent'})


def get_tiktok_video(url, storage_location):
	cwd = os.getcwd()
	if not os.path.exists(storage_location):
		os.makedirs(storage_location)
	os.chdir(storage_location)
	if url.endswith("/"):
		url = url[:-1]
	__, name = url.rsplit("/", 1)
	name= name+".mp4"
	parent = bs(session.get(url).text, features="html5lib") 
	urllib.request.urlretrieve(parent.find("video")["src"], name)
	os.chdir(cwd)
	return True

def test_func():
	url = ""
	storage_location = ""
	get_tiktok_video(url, storage_location)

if __name__ == '__main__':
	test_func()

