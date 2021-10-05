import urllib.request
import requests
from bs4 import BeautifulSoup as bs
import os
import csv
import youtube_dl
from datetime import datetime as dt
import re
import json
import pprint
import csv

session = requests.Session()
session.headers.update({'User-Agent': 'Custom user agent'})

agent_name = "tiktok_harvesters_2"
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





def get_tiktok_videos(item):
	print("tiktok")
	"""
	Gets a single video from a given tiktok page URL
	Attempts to download tiktok video from tiktok url
	Updates the item() data object
	
	"""
	
	url = item.url
	storage_folder = item.storage_folder
	#storage_location = item.storage_location
	item.agent_name = agent_name+"_get_video"
	cwd = os.getcwd()
	#print(storage_location)
	if not os.path.exists(storage_folder):
		os.makedirs(storage_folder)
	os.chdir(storage_folder)
	if url.endswith("/"):
		url = url[:-1]
	__, name = url.rsplit("/", 1)
	print(url)
	name = name+".mp4"
	parent = bs(session.get(url).text, features="html5lib") 
	res = parent.find("script",attrs={"crossorigin":"anonymous"})
	print(res.contents)
	json_object = json.loads(res.contents[0])
	items = json_object["props"]["pageProps"]["items"]
	video_collector(items, storage_folder, item)
	os.chdir(cwd)
	item.completed = True
	return item

def video_collector(items, storage_folder ,item):

	""" 
	Collects videos, video infromation, comments information and writes it to json files. Writes errors to error file.
	Arguments:
		video_ids(list) - dictionaries to collect
		storage_folder(str) - location of folder where to collect
		item(obj) 
	Returns:
		flag (bool) - true if everything collected, false if any error


	"""

	storage_folder = "."
	flag = True
	csv_rows = []
	for itm in items:
		flag=True
		vidid=itm["id"]
		print(vidid)
		csv_row = []
		csv_row.append(item.id)
		csv_row.append(vidid)
		csv_row.append(dt.now().strftime('%Y%m%d %H:%M:%S'))
		print(csv_row)
		ydl = youtube_dl.YoutubeDL({'outtmpl':os.path.join(storage_folder, vidid, vidid+'.'+'%(ext)s')})
		url = item.url.rstrip("?")+"/video/"+vidid
		try:
			ydl.download([url])	
			csv_row.append("True")
		except Exception as e:
			csv_row.append('False')
			print(str(e))
			print(vidid)
			with open(os.path.join(storage_folder,'errors_{}.txt'.format(dt.now().strftime('%Y%m%d'))), "a") as f:
				f.write(vidid + "|" + item.id + " " + str(e) )
				f.write("\n")
				flag = False
		csv_rows.append(csv_row)
		if flag:
			with open(os.path.join(storage_folder, vidid,vidid+'_metadata_{}.json'.format(dt.now().strftime('%Y%m%d'))), 'w') as json_file:
				json.dump(itm, json_file)	
	with open (os.path.join(storage_folder, item.id+'.csv'), 'a') as f:
		csv_writer = csv.writer(f, quoting=csv.QUOTE_NONE)
		csv_writer.writerows(csv_rows)
					
	return flag
	


