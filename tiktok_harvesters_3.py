import urllib.request
import requests
from bs4 import BeautifulSoup as bs
import os
import csv
import yt_dlp
from datetime import datetime as dt
import re
import json
import pprint
import csv
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
session = requests.Session()
session.headers.update({'User-Agent': 'Custom user agent'})

agent_name = "tiktok_harvesters_3"


ydl_opts = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    'outtmpl': '%(title)s.%(ext)s',
    'ignoreerrors': True,
    'writedescription': True,
    'nocheckcertificate': True,
    'writecomments': True,
    'writedescription': True,
    'writeinfojson': True,
    'mergeoutputformat': 'mp4',
}

print(ydl_opts)



def get_tiktok_video(item):

	"""
	Managing collecting of single video
	Arguments:
		item (obj) - contains row data from spreadsheet
	Returns:
		item (obj) - contains row data from spreadsheet with "completed" set True or False
	"""
	print(item.id)
	print("Video")

	item.agent_name = agent_name+"_get_video"
	storage_folder = item.storage_folder
	flag=True
	url = item.url
	vidid=url.split("/")[-1]
	if not os.path.exists(storage_folder):
		os.makedirs(storage_folder)

	my_path = os.path.join(storage_folder, vidid+'.'+'%(ext)s')
	print(my_path)
	try:

		ydl_opts['outtmpl']=my_path
		print(ydl_opts)
		ydl = yt_dlp.YoutubeDL(ydl_opts)
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



