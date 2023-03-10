import subprocess
import configparser
import os
import sys
import json
import csv
import requests
from time import sleep
from datetime import datetime as dt
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import requests
from urllib.request import urlopen
import yt_dlp
import PySimpleGUI as sg
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
session = requests.Session()

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

def my_gui():

	form = sg.FlexForm('form name')
	scheme = "LightGreen2"
	sg.theme(scheme)
	value_list = ["value1", "value2"]
	layout = [

			[sg.Text('Insert link to tiktok web page',font = ('Helvetica', 13, 'bold italic'))],
			[sg.Text('Full path with tag or username',font = ('Helvetica', 11, 'italic'))],
			[sg.Text('Tiktok link', size=(10, 1)), sg.InputText("https://www.tiktok.com/@laahhmcconville",key='url',size=(100, 1))],
			[sg.Text('', size=(100, 1)),sg.FolderBrowse('FolderBrowse',key='foldername')],
			[sg.Button("Run!")]

		]
	window =sg.Window(f'TikTok downloader', layout, default_element_size=(35, 2))#,background_color='#ACBAAB')
	event,values=window.read()

	return values,window,event
 






def get_tiktok_videos(url, storage_folder):

	"""
	Gets a single video from a given tiktok page URL
	Attempts to download tiktok video from tiktok url
	Updates the item() data object
	
	"""
	flag_collected = False
	print(url)
	items = []
	driver = webdriver.Firefox()
	print("here1")
	if not os.path.exists(storage_folder):
		os.makedirs(storage_folder)
	downloaded_files = os.listdir(storage_folder)
	print("here2")
	driver.set_window_size(768,1024)
	driver.get(url)
	driver.maximize_window()
	sleep(2)
	driver.get(url)
	sleep(15)
	scroll_down(driver)
	my_links = []
	my_links_dict = {}
	print("here5")
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


	video_collector(items, storage_folder, itms_titles, downloaded_files )
	file_collected = True
	return flag



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

def download_video(link,  video_path, video_folder):
	print("here!!!")
	print(link)
	print(video_path)
	print(video_folder)
	if not os.path.exists(video_folder):
		os.makedirs(video_folder)
	try:
		ydl_opts['outtmpl']=video_path
		print(ydl_opts)
		ydl = yt_dlp.YoutubeDL(ydl_opts)
		ydl.download([link])	
		flag = True
	except:
		flag = False
	return flag


def parse_link(storage_folder,video_id):

	video_path =  os.path.join(storage_folder, video_id, video_id+".mp4")
	video_folder = os.path.join(storage_folder, video_id )
	return(video_path, video_folder)

def video_collector(items, storage_folder, itms_titles, downladed_files ):

	"""Gets list of video links and then downloads each video. Set item.flag = True if complete."""

	print("Videos")
	print(os.getcwd())

	if not os.path.exists(storage_folder):
		os.makedirs(storage_folder)
	downloaded_files = os.listdir(storage_folder)


	for itm in items:
		print(itm)
		sg.Print("Collecting " + itm)
		video_id = itm.split("/")[-3].lstrip("@")+"_"+itm.split("/")[-1]
		if not video_id in downloaded_files:
			download_path, download_folder = parse_link(storage_folder, video_id)
			flag = download_video(itm,  download_path,download_folder)
			if not os.path.exists(download_path) or os.path.getsize(download_path)==0:
				flag = download_video(itm,  download_path, download_folder)
			if  flag:
				with open(os.path.join(storage_folder,"links_processed.txt"),"a") as f:
						f.write(itm)
						f.write("\n")
				with open(os.path.join(storage_folder,"links_titles.txt"), "a",encoding="UTF-8") as f:
						f.write(itm +"|||"+itms_titles[itm])
						f.write("\n")

	completed_flag = flag

	return flag

def main():

	values,window,event = my_gui()
	foldername = values["foldername"]
	url = values["url"]
	sg.Print('Collecting from ', url)
	get_tiktok_videos( url, foldername)
	sg.Print("Done!")
	window.close()	


if __name__ == '__main__':

	main()