import io
import json
import csv
import os
import time
import requests
import youtube_dl
import dateparser
import sys
# from bs4 import BeautifulSoup as bs
# from selenium import webdriver
# from apiclient.discovery import build
from datetime import datetime as dt
from datetime import timezone
sys.path.insert(0, r'C:\Source\secrets_and_credentials')
# from api import api_key

# youtube = build('youtube',"v3", developerKey=api_key)

agent_name = "vimeo_harvesters"




def get_channel(item):

	"""
	Getting video ids from channel
	Arguments:
		item (obj) - contains row data from spreadsheet
	Returns:
		item (obj) - contains row data from spreadsheet with "completed" set True or False
	"""
	print(item.id)
	print("Vimeo channel")
	video_ids = []
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
		print("herr2")
		ydl_opts = {
				'ignoreerrors': True,
					'quiet': True
					}
		ydl = youtube_dl.YoutubeDL(ydl_opts)


		result = ydl.extract_info(
											url,
											download = False
											)

		if 'entries' in result:
			
			videos = result ['entries']
	
		print(len(videos))
		print("here21")
		for video in videos:
			print(video)
			print("here23")
			vidid = video["id"]
			print(vidid)
			if not vidid in video_ids:
				
				upload_date = video["upload_date"]
				print("here22")
				print(upload_date)
				if not item.archived_start_date or upload_date > item.archived_start_date:
					video_ids.append(vidid)
		print("go to video collector")
		flag = video_collector(video_ids, storage_folder, item.id)
		os.chdir(cwd)
		item.completed = flag
	except:
		os.chdir(cwd)
		item.completed = False
	return item

def get_video(item):
	print("Vimeo video")
	print(item.id)

	"""
	Managing collecting of single video
	Arguments:
		item (obj) - contains row data from spreadsheet
	Returns:
		item (obj) - contains row data from spreadsheet with "completed" set True or False
	"""
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
		video_ids= [url.split('/')[-1]]
		video_collector(video_ids, storage_folder, item.id)

		os.chdir(cwd)
		item.completed = True
	except:
		os.chdir(cwd)
		item.completed = False
	return item



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
	print(video_ids)
	storage_folder = "."
	#ydl = youtube_dl.YoutubeDL({'outtmpl':os.path.join(storage_folder,'%(id)s.%(ext)s')})
	flag = True
	csv_rows = []
	for vidid in video_ids:
		videos = []
		csv_row = []
		csv_row.append(id)
		csv_row.append(vidid)
		csv_row.append(dt.now().strftime('%Y%m%d %H:%M:%S'))
		print(csv_row)
		url = "https://vimeo.com/"+vidid
		ydl = youtube_dl.YoutubeDL({'outtmpl':os.path.join(storage_folder,vidid,'%(id)s.%(ext)s')})
		try:

			result = ydl.extract_info(
												url,
												download = True
												)
			print("checking entries")
			if 'entries' in result:
				print("here entries")
				videos = result ['entries']
			else:
				videos  = result
			print("let us write to file")
			with open(os.path.join(storage_folder,vidid, vidid+'.json'), 'w') as json_file:
				json.dump(videos, json_file)
			print("done")



		except Exception as e:
			print(str(e))
			with open(os.path.join(storage_folder,id,'errors_{}.txt'.format(dt.now().strftime('%Y%m%d'))), "a") as f:
				f.write( id + " " + str(e) )
				f.write("\n")
				flag = False
		if videos:
			if videos == []:
				csv_row.append("Fasle")
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

