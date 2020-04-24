import io
import json
import csv
import os
import time
import requests
import youtube_dl
import dateparser
import sys
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from apiclient.discovery import build
from datetime import datetime as dt
sys.path.insert(0, r'C:\Source\secrets_and_credentials')
from api import api_key

youtube = build('youtube',"v3", developerKey=api_key)

def get_video(item):


	"""
	Managing collecting of single video
	Arguments:
		item (obj) - contains row data from spreadsheet
	Returns:
		item (obj) - contains row data from spreadsheet with "completed" set True or False
	"""

	url = item.url
	storage_folder_root = item.storage_folder_root
	try:
		cwd = os.getcwd()
		if not os.path.exists(storage_folder_root):
			os.makedirs(storage_folder_root)
		os.chdir(storage_folder_root)
		if url.endswith("/"):
			url = url[:-1]
		video_ids= [link.split('?v=')[-1].split("&")[0]]
		video_collector(video_ids)
		os.chdir(cwd)
		item.completed = True
	except:
		os.chdir(cwd)
		item.completed = False
	return item

def get_channel(item):

	"""
	Getting video ids from channel
	Arguments:
		item (obj) - contains row data from spreadsheet
	Returns:
		item (obj) - contains row data from spreadsheet with "completed" set True or False
	"""

	url = item.url
	storage_folder_root = item.storage_folder_root
	try:
		cwd = os.getcwd()
		if not os.path.exists(storage_folder_root):
			os.makedirs(storage_folder_root)
		os.chdir(storage_folder_root)
		if url.endswith("/"):
			url = url[:-1]

		channel_id = link.split("channel/")[-1].split("/")[0]
		req = youtube.channels().list(id = self.channel_id, part = 'contentDetails')
		result = req.execute()
		playlist = result["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
		videos = []
		next_page_token = None
		while 1:
			res = youtube.playlistItems().list(playlistId= playlist, part="snippet", maxResults=50 , pageToken=next_page_token).execute()
			videos += res["items"]
			try:
				next_page_token = res["nextPageToken"]
			except:
				next_page_token = None
			if next_page_token is None:
				break
		video_ids = get_ids_from_videos(videos)
		video_collector(video_ids)
		os.chdir(cwd)
		item.completed = True
	except:
		os.chdir(cwd)
		item.completed = False
	return item

def get_user(item):

	"""
	Collects video ids from youtube user, pass them for downloading and returns flag and location
	Returns:
	flag(bool) - true if successful
	location   - location of folder with downloaded materials

	"""
	try:
		cwd = os.getcwd()
		if not os.path.exists(storage_location):
			os.makedirs(storage_location)
		os.chdir(storage_location)
		if url.endswith("/"):
			url = url[:-1]
		link_list = []	
		all_video_ids = []
		driver=webdriver.Chrome()
		driver.get(self.link)
		offset = 0
		driver.maximize_window()
		max_window_height = driver.execute_script('return Math.max('
		                                                      'document.body.scrollHeight, '
		                                                      'document.body.offsetHeight, '
		                                                      'document.documentElement.clientHeight, '
		                                                      'document.documentElement.scrollHeight, '
		                                                      'document.documentElement.offsetHeight);')
		height = driver.execute_script('return Math.max(''document.documentElement.clientHeight, window.innerHeight);')
		count= 0
		offset = int(height)
		for n in range(30):
			count+=1
			if count <15:
				driver.execute_script('window.scrollTo(0, {});'.format(offset))
				time.sleep(1)
				offset+=height
				html = driver.page_source
				soup = bs(html)
				all_youtube_links = soup.findAll({"a":{"id":"video-title"}})
				for el in all_youtube_links:
					if "href" in el.attrs.keys() and "/watch?v=" in el.attrs["href"] and not "&" in el.attrs["href"]:
						if not el.attrs["href"] in link_list:
							all_video_ids += [el.attrs["href"].split("/watch?v=")[-1]]
		if item.archived_start_date:
			video_ids = filter_user_video_by_date(all_video_ids, item.archived_start_date)
		else:
			vide_ids = all_video_ids
		video_collector(video_ids)
		os.chdir(cwd)
		item.completed = True
	except:
		os.chdir(cwd)
		item.completed = False
	return item

def filter_user_video_by_date(all_video_ids, archived_start_date):
	"""
		Creating list of videos published after archived_start_date
	Args:
		all_video_ids (lst) - users all video ids
		archived_start_date (dateparser(obj)) - 
	"""


	video_ids = []
	for vidid in all_video_ids:
		try:
			res = youtube.videos().list(id = vidid, part = "snippet").execute()
		except:
			youtube = build('youtube',"v3", developerKey=api_key)
			res = youtube.videos().list(id = vidid, part = "snippet").execute()
		published_at =  dateparser.parse(res["items"][0]["snippet"]["publishedAt"])
			
		if published_at > archived_start_date:
			video_ids += vidid
	return(video_ids)


def get_ids_from_videos(videos):

	"""Making list of video ids from channel from certain date"""

	for video in videos:
		video_time_stamp = time.mktime(dt.strptime(video["snippet"]["publishedAt"],"%Y-%m-%dT%H:%M:%S.000Z").timetuple())
		
		if video_time_stamp > item.from_date_stamp:
			self.video_ids += [video["snippet"]["resourceId"]["videoId"]]

def get_video_comments(youtube, **kwargs):

	"""Collects comments info by video id
	Args:
		kwargs (parameters )
	Return:
		comments (list) - comments thread in json format
	"""
	comments = []
	results = youtube.commentThreads().list(**kwargs).execute()

	while results:
		for item in results['items']:
			comment = item['snippet']['topLevelComment']['snippet']#['textDisplay']
			comments.append(comment)

		if 'nextPageToken' in results:
			kwargs['pageToken'] = results['nextPageToken']
			results = youtube.commentThreads().list(**kwargs).execute()
		else:
			break
	return comments

		


def video_collector(video_ids):

	""" 
	Rounting the collecting process
		Returns:

	"""
	ydl = youtube_dl.YoutubeDL({'outtmpl':os.path.join(project_folder,str(ui),"files",'%(id)s.%(ext)s')})
	json_data = []
	comments_data = []
	flag = True
	for vidid in self.video_ids:
		url = "https://www.youtube.com/watch?v="+vidid
		try:
			res = youtube.videos().list(id = vidid, part = "snippet").execute()
		except Exception as e:
			youtube = build('youtube',"v3", developerKey=api_key)
			res = youtube.videos().list(id = vidid, part = "snippet").execute()
		json_data.append(res)
		try:
			comments_data.append(get_video_comments(youtube, part='snippet', videoId=vidid))
		except Exception as e:
			print(str(e))
			print(vidid)
			with open(os.path.join(ui_folder,'errors_{}.txt'.dt.now().strftime('%Y%m%d')), "a") as f:
				f.write(vidid + "|" + ui + " " + str(e) )
				f.write("\n")
		try:
			ydl.download([url])	
		except Exception as e:
			print(str(e))
			print(vidid)
			with open(os.path.join(ui_folder,'errors_{}.txt'.dt.now().strftime('%Y%m%d')), "a") as f:
				f.write(vidid + "|" + ui + " " + str(e) )
				f.write("\n")
				flag = False					
	with open(os.path.join(ui_folder, str(ui)+'.json'), 'a') as json_file:
		json.dump(json_data, json_file)
	with open(os.path.join(ui_folder, str(ui)+'_comments.json'), 'a') as json_file:
		json.dump(comments_data, json_file)
	

def main():
	pass
	# item = {
	# 	"url":"https://twitter.com/ndha_nz",
	# 	"storage_folder":"./junk",
	# 	"date_range":"01.03.2020"
	# 	}

	# print (item)
	# get_account(item)
	# # get_tweet(item)


if __name__ == '__main__':
	main()	

