import subprocess
import configparser
import os
import sys
import json
import csv
import requests
from time import sleep
import yt_dlp
from datetime import datetime as dt
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import requests
from urllib.request import urlopen
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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


agent_name = "tiktok_harvesters_3"
secrets_and_credentials_fold = r'C:\Source\sercrets_and_credentials'
script_folder = os.getcwd()
config = configparser.ConfigParser()
config.read(os.path.join(secrets_and_credentials_fold,"secret"))
	


def get_tiktok_videos(item):

	"""
	Gets a single video from a given tiktok page URL
	Attempts to download tiktok video from tiktok url
	Updates the item() data object
	
	"""
	print("Tiktok videos")
	url = item.url
	storage_folder = item.storage_folder
	#storage_location = item.storage_location
	item.agent_name = agent_name+"_get_video"
	wd = os.getcwd()
	#print(storage_location)
	if not os.path.exists(storage_folder):
		os.makedirs(storage_folder)
	if url.endswith("/"):
		url = url[:-1]
	__, name = url.rsplit("/", 1)
	print(url)
	items = []
	name = name+".mp4"
	driver = webdriver.Firefox()
	if not os.path.exists(item.storage_folder):
		os.makedirs(item.storage_folder)
	downloaded_files = os.listdir(item.storage_folder)
	driver.set_window_size(768,1024)
	driver.get(item.url)
	driver.maximize_window()
	sleep(2)
	driver.get(item.url)
	sleep(15)
	scroll_down(driver)
	my_links = []
	my_links_dict = {}
	soup = bs(driver.page_source, 'html.parser')
	print(soup.text)
	items = []
	itms_titles={}
	lnks_soup = soup.find_all("div",attrs={"class":"tiktok-x6y88p-DivItemContainerV2 e19c29qe7"})
	for lnk_soup in lnks_soup:
		lnk=lnk_soup.find("a").attrs["href"]
		print(lnk)
		items.append(lnk)
		title = lnk_soup.find("img").attrs["alt"]
		print(title)
		itms_titles[lnk]=title


	video_collector(items, storage_folder, itms_titles, downloaded_files ,item )
	item.completed = True
	return item



def scroll_down(driver):

    """
    A method for scrolling the page.
    Origin: #https://stackoverflow.com/questions/48850974/selenium-scroll-to-end-of-page-in-dynamically-loading-webpage
    """

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(6)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def download_video(link ,  video_path,  video_folder):


	try:
		if not os.path.exists(video_folder):
			os.makedirs(video_folder)

		ydl_opts['outtmpl']=video_path
		print(ydl_opts)
		ydl = yt_dlp.YoutubeDL(ydl_opts)
		ydl.download([link])	
		flag = True
	except Exception as e:
			print(str(e))
			print(link)
			with open(os.path.join(video_folder,'errors_{}.txt'.format(dt.now().strftime('%Y%m%d'))), "a") as f:
				f.write(link + "|" + str(e) )
				f.write("\n")
			flag = False
	return flag
		


def parse_link(storage_folder,video_id):

	video_path =  os.path.join(storage_folder, video_id, video_id+".mp4")
	video_folder = os.path.join(storage_folder, video_id )
	return(video_path, video_folder)

def video_collector(items, storage_folder, itms_titles, downladed_files ,item):

	"""Gets list of video links and then downloads each video. Set item.flag = True if complete."""
	
	print(item.id)
	print("Videos")
	print(os.getcwd())
	item.agent_name = agent_name+"_get_videos"
	if not os.path.exists(item.storage_folder):
		os.makedirs(item.storage_folder)
	downloaded_files = os.listdir(item.storage_folder)

	
	for itm in items:
		print(itm)

		video_id = itm.split("/")[-3].lstrip("@")+"_"+itm.split("/")[-1]
		if not video_id in downloaded_files:
			download_path, download_folder = parse_link(item.storage_folder, video_id)
			flag = download_video(itm,  download_path, download_folder)
			if not os.path.exists(download_path) or os.path.getsize(download_path)==0:
				flag = download_video(itm,  download_path, download_folder)
			if  flag:
				with open(os.path.join(storage_folder,"links_processed.txt"),"a") as f:
						f.write(itm)
						f.write("\n")
				with open(os.path.join(storage_folder,"links_titles.txt"), "a",encoding="UTF-8") as f:
						f.write(itm +"|||"+itms_titles[itm])
						f.write("\n")

	item.completed = flag

	return item

