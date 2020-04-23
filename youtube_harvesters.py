import io
import json
import csv
import os
import time
import requests
import youtube_dl
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from apiclient.discovery import build
from datetime import datetime as dt
from api import api_key

youtube = build('youtube',"v3", developerKey=api_key)

class Youtube_harvester():

	def __init__(self, data):

		"""
		Manages youtube harvesting processes

		Arguments:
		    data (list) - a row from google spreadsheet

		Return:
			location (str) - storage location
			flag (bool) - True if successful otherwise False

		"""
		self.data = data
		self.ui = self.data[0]
		self.description = self.data[1]
		self.creator = self.data[2]
		self.ready = self.data[3]
		self.category = self.data[4]
		self.location = self.data[5]
		self.content_type = self.data[6]
		self.link = self.data[7]
		self.date_range = self.data[8]
		self.recurring = self.data[9]
		self.sccope = self.data[10]
		self.archived = self.data[11]
		self.collected = self.data[12]
		self.responsible	= self.data[13]
		self.storage_location = self.data[14]
		self.notes = self.data[15]
		self.repeating = self.data[16]
		self.row_number = self.data[17]
		self.project_folder = self.data[18]
		self.ui_folder = os.path.join(self.project_folder, self.ui)
		self.file_folder = os.path.join(self.ui_folder, "files")
		if not os.path.isdir(self.project_folder):
			os.mkdir(self.project_folder)
		self.video_ids = []
		self.start_time = dt.strptime("19900101","%Y%m%d").strftime('%Y-%m-%dT%H:%M:%SZ')
		if self.repeating:
			self.start_time = dt.strptime(self.date_range.split("onward")[0].rstrip(" "),"%d.%m.%Y").strftime('%Y-%m-%dT%H:%M:%SZ')
			if self.archived != "":
				self.start_time = dt.strptime(self.archived,"%d.%m.%Y").strftime('%Y-%m-%dT%H:%M:%SZ')
		print(self.start_time)
		self.from_date_stamp = time.mktime(dt.strptime(self.start_time,"%Y-%m-%dT%H:%M:%SZ").timetuple())


	def youtube_video(self):

		"""
		Managing collecting of single video
		Returns:
			flag(bool) - true if successful
			location   - location of folder with downloaded materials
		"""

		
		self.video_ids= [link.split('?v=')[-1].split("&")[0]]
		self.video_collector()
		return(slef.flag, self.ui_folder)

	def youtube_channel(self):

		"""Getting video ids from channel"""

		self.channel_id = link.split("channel/")[-1].split("/")[0]
		req = youtube.channels().list(id = self.channel_id, part = 'contentDetails')
		result = req.execute()
		playlist = result["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
		videos = []
		next_page_token = None
		while 1:
			res = youtube.playlistItems().list(playlistId= playlist, part="snippet", maxResults=50 , pageToken=next_page_token).execute()
			videos += res["items"]
			print(res.keys())
			try:
				next_page_token = res["nextPageToken"]
			except:
				next_page_token = None
			if next_page_token is None:
				break
		self.videos = videos
		get_ids_from_videos()
		self.video_collector()
		return flag, self.ui_folder

	def youtube_user(self):

		"""
		Collects video ids from youtube user, pass them for downloading and returns flag and location
		Returns:
		flag(bool) - true if successful
		location   - location of folder with downloaded materials

		"""
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
			if count <20:
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
		self.all_video_ids = all_video_ids
		self.filter_user_video_by_date()
		self.video_collector()
		return self.flag, self.ui_folder

	def filter_user_video_by_date(self):

		for vidid in self.all_video_ids:
			try:
				res = youtube.videos().list(id = vidid, part = "snippet").execute()
			except:
				youtube = build('youtube',"v3", developerKey=api_key)
				res = youtube.videos().list(id = vidid, part = "snippet").execute()
			published_at = res["items"][0]["snippet"]["publishedAt"]
			try:
				published_at_timestamp = time.mktime(dt.strptime(published_at,"%Y-%m-%dT%H:%M:%S.000Z").timetuple())
			except:
				published_at_timestamp = time.mktime(dt.strptime(published_at,"%Y-%m-%dT%H:%M:%SZ").timetuple())
			
			if published_at_timestamp > self.from_date_stamp:
				self.video_ids += vidid


	def get_ids_from_videos(self):

		"""Making list of video ids from channel from certain date"""

		for video in self.videos:
			video_time_stamp = time.mktime(dt.strptime(video["snippet"]["publishedAt"],"%Y-%m-%dT%H:%M:%S.000Z").timetuple())
			
			if video_time_stamp > self.from_date_stamp:
				self.video_ids += [video["snippet"]["resourceId"]["videoId"]]

	def get_video_comments(youtube, **kwargs):

		"""Collects comments info by video id
		Args:
			kwargs (parameters )
		Return:
			comments (list) - comments thread in json format
		"""
		self.comments = []
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

		self.comments= comments


	def video_collector(self):

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
			self.flag = flag

			

