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
from datetime import timezone
sys.path.insert(0, r'C:\Source\secrets_and_credentials')
from api import api_key

youtube = build('youtube',"v3", developerKey=api_key)

agent_name = "youtube_harvesters"

def get_video(item):


	"""
	Managing collecting of single video
	Arguments:
		item (obj) - contains row data from spreadsheet
	Returns:
		item (obj) - contains row data from spreadsheet with "completed" set True or False
	"""
	print(item.id)
	print("Video")
	url = item.url
	item.agent_name = agent_name+"_get_video"
	storage_folder = item.storage_folder
	try:
		cwd = os.getcwd()
		if not os.path.exists(storage_folder):
			os.makedirs(storage_folder)
		os.chdir(storage_folder)
		if url.endswith("/"):
			url = url[:-1]
		video_ids= [url.split('?v=')[-1].split("&")[0]]
		video_collector(video_ids, storage_folder, item.id)
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
	print(item.id)
	print("Channel")
	url = item.url
	item.agent_name = agent_name+"_get_channel"
	storage_folder = item.storage_folder
	try:
		cwd = os.getcwd()
		if not os.path.exists(storage_folder):
			os.makedirs(storage_folder)
		os.chdir(storage_folder)
		if url.endswith("/"):
			url = url[:-1]
		channel_id = url.split("channel/")[-1].split("/")[0]
		req = youtube.channels().list(id = channel_id, part = 'contentDetails')
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
		video_ids = get_ids_from_videos(videos, item.archived_start_date)
		print("go to video collector")
		flag = video_collector(video_ids, storage_folder, item.id)
		os.chdir(cwd)
		item.completed = flag
	except:
		os.chdir(cwd)
		item.completed = False
	return item

def get_playlist(item):

	"""
	Getting video ids from channel
	Arguments:
		item (obj) - contains row data from spreadsheet
	Returns:
		item (obj) - contains row data from spreadsheet with "completed" set True or False
	"""
	print(item.id)
	print("Playlist")
	url = item.url
	item.agent_name = agent_name+"_get_playlist"
	storage_folder = item.storage_folder
	try:
		cwd = os.getcwd()
		if not os.path.exists(storage_folder):
			os.makedirs(storage_folder)
		os.chdir(storage_folder)
		if url.endswith("/"):
			url = url[:-1]
		playlist_id = url.split("?list=")[-1].split("/")[0]
		videos = []
		next_page_token = None
		while 1:
			res = youtube.playlistItems().list(playlistId= playlist_id, part="snippet", maxResults=50 , pageToken=next_page_token).execute()
			videos += res["items"]
			try:
				next_page_token = res["nextPageToken"]
			except:
				next_page_token = None
			if next_page_token is None:
				break
		video_ids = get_ids_from_videos(videos, item.archived_start_date)
		#print(video_ids)
		flag = video_collector(video_ids, storage_folder, item.id)
		os.chdir(cwd)
		item.completed = flag
	except Exception as e:
		print(str(e))
		os.chdir(cwd)
		item.completed = False
	return item

def get_user(item):

	"""
	Collects video ids from youtube user, pass them for downloading and returns flag and location
	Arguments:
		item (obj) - contains row data from spreadsheet
	Returns:
		item (obj) - contains row data from spreadsheet with "completed" set True or False


	"""
	print(item.id)
	print("User")
	item.agent_name = agent_name+"_get_user"
	try:
		cwd = os.getcwd()
		if not os.path.exists(item.storage_folder):
			os.makedirs(item.storage_folder)
		os.chdir(item.storage_folder)
		link_list = []	
		all_video_ids = []
		driver=webdriver.Chrome()
		driver.get(item.url)
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
		all_video_ids = []
		for n in range(10):
			count+=1
			if count <10:
				driver.execute_script('window.scrollTo(0, {});'.format(offset))
				time.sleep(1)
				offset+=height
				html = driver.page_source
				soup = bs(html)
				all_youtube_links = soup.findAll({"a":{"id":"video-title"}})
				for el in all_youtube_links:
					if "href" in el.attrs.keys() and "/watch?v=" in el.attrs["href"] and not "&" in el.attrs["href"]:
						if not el.attrs["href"].split("/watch?v=")[-1] in all_video_ids:
							all_video_ids += [el.attrs["href"].split("/watch?v=")[-1]]
		all_video_ids = list(set(all_video_ids))
		driver.close()
		if item.archived_start_date:
			video_ids = filter_user_video_by_date(all_video_ids, item.archived_start_date)
		else:
			video_ids = all_video_ids
		flag = video_collector(video_ids, item.storage_folder, item.id)
		os.chdir(cwd)
		item.completed = flag
	except Exception as e:
		print(str(e))
		os.chdir(cwd)
		item.completed = False
	return item

def filter_user_video_by_date(all_video_ids, archived_start_date):
	"""
		Creating list of videos published after archived_start_date
	Args:
		all_video_ids (lst) - users all video ids
		archived_start_date (datetime(obj)) -  date where to start collection
	Returns:
		video_ids (list) - contains all individual video ids to collect

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


def get_ids_from_videos(videos, archived_start_date):

	"""

	Making list of video ids from channel from certain date
	Arguments:
		videos (json) - individual video information		
		archived_start_date (datetime(obj)) -  date where to start collection
	Returns:
		video_ids (list) - contains all individual video ids to collect

	"""
	video_ids = []
	for video in videos:
		video_time = dateparser.parse(video["snippet"]["publishedAt"])
		try:
			print(video_time > archived_start_date)
		except Exception as e:
			try:
				video_time=dateparser.parse(video_time.strftime('%Y-%m-%d %H:%M:%S'))
			except Exception as e:
				print(str(e))
		if archived_start_date == None or video_time > archived_start_date:
			video_ids += [video["snippet"]["resourceId"]["videoId"]]
	return video_ids

def get_video_comments(youtube, **kwargs):

	"""Collects comments info by video id
	Args:
		kwargs (parameters )
	Return:
		comments (list) - comments thread in json format
	"""
	comments = []
	try:
		results = youtube.commentThreads().list(**kwargs).execute()
	except Exception as e:
		print (str(e))
		youtube = build('youtube',"v3", developerKey=api_key)
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

		


def video_collector(video_ids, storage_folder ,id):

	""" 
	Collects videos, video infromation, comments information and writes it to json files. Writes errors to error file.
	Arguments:
		video_ids(list) - list of video_ids to collect
		storage_folder(str) - location of folder where to collect
		id(str) - unique identifier
	Returns:
		flag (bool) - true if everything collected, false if any error


	"""

	storage_folder = "."
	flag = True
	print(video_ids)
	csv_rows = []
	for vidid in video_ids:
		print(vidid)
		res= None
		comments = None
		csv_row = []
		csv_row.append(id)
		csv_row.append(vidid)
		csv_row.append(dt.now().strftime('%Y%m%d %H:%M:%S'))
		print(csv_row)
		ydl = youtube_dl.YoutubeDL({'outtmpl':os.path.join(storage_folder, vidid, vidid+'.'+'%(ext)s')})
		url = "https://www.youtube.com/watch?v="+vidid
		try:
			ydl.download([url])	
			csv_row.append("True")


		except Exception as e:
			csv_row.append('False')
			print(str(e))
			print(vidid)
			with open(os.path.join(storage_folder, vidid,'errors_{}.txt'.format(dt.now().strftime('%Y%m%d'))), "a") as f:
				f.write(vidid + "|" + id + " " + str(e) )
				f.write("\n")
				flag = False					
		try:
			res = youtube.videos().list(id = vidid, part = "snippet").execute()
			
		except Exception as e:
			youtube = build('youtube',"v3", developerKey=api_key)
			try:
				res = youtube.videos().list(id = vidid, part = "snippet").execute()
			except Exception as e:
				pass
		
		if res:
			if res == []:
				csv_row.append("False")
			else:
				csv_row.append('True')
		else:
			csv_row.append("False")
		print(csv_row)
		with open(os.path.join(storage_folder, vidid, vidid+'.json'), 'w') as json_file:
			json.dump(res, json_file)
		try:
			comments = get_video_comments(youtube, part='snippet', videoId=vidid)
			with open(os.path.join(storage_folder, vidid, vidid+'_comments.json'), 'w') as json_file:
				json.dump(comments, json_file)

		except Exception as e:
			print(str(e))
			print(vidid)
			with open(os.path.join(storage_folder, vidid,'errors_{}.txt'.format(dt.now().strftime('%Y%m%d'))), "a") as f:
				f.write(vidid + "|" + id + " " + str(e) )
				f.write("\n")
		
		if comments:
			if comments == []:
				csv_row.append("False")
			else:
				csv_row.append('True')
		else:
			csv_row.append("False")
		print(csv_row)
		csv_rows.append(csv_row)
	print(csv_rows)
	print(os.path.join(storage_folder, id+'.csv'))
	with open (os.path.join(storage_folder, id+'.csv'), 'a') as f:
		csv_writer = csv.writer(f, quoting=csv.QUOTE_NONE)
		#csv_writer.writerow (["Id","Video id","Date Time", "Video", "Metadata", "Comments"]) # write header
		csv_writer.writerows(csv_rows)
	return flag
	

def main():
	pass



if __name__ == '__main__':
	main()	

