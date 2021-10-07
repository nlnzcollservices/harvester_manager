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
#import fbdown

# sys.path.insert(0,r'C:\Users\Korotesv\fbdown')
# from fbdown import TheMain as fbdown

agent_name = "facebook_harvesters_2"
secrets_and_credentials_fold = 'C:\Source\sercrets_and_credentials'
script_folder = os.getcwd()
config = configparser.ConfigParser()
config.read(os.path.join(secrets_and_credentials_fold,"secret"))
facebook_login =config.get( "social_media_harvester", "facebook_login") 
facebook_password= config.get("social_media_harvester", "facebook_password")	

def get_video(item):

	"""
	Gets a single video from a given facebook video page URL
	Has 3 steps. 
	1. Attempts to find facebook video ID from given URL, 
	2. Attemps to download that video binary from the video id via the fbdown tool (commandline call)
	https://tbhaxor.github.io/fbdown/
	3. Updates the item() data object
	
	todo
	Resulting data needs to reshaped into standardised format
	URL cleanup could be better
	"""
	try:
		if not 'facebook.com' in item.url:
			r = requests.get(item.url)
			url = r.url
		else:
			url = item.url
		storage_location = item.storage_location
		item.agent_name = agent_name+"_get_video"
		cwd = os.getcwd()
		#item.storage_folder = item.storage_folder.replace("/","\\")
		if not os.path.exists(item.storage_folder):
			os.makedirs(item.storage_folder)
		os.chdir(item.storage_folder)
		item.storage_location = os.getcwd()
		print(item.storage_location)
		if url.endswith("/"):
			url = url[:-1]
		__, user_name = url.rsplit("/", 1)
		print(user_name)
		print("here")
		name = user_name.replace("?", "_").replace("=", "_").replace("?", "_").replace("=","_")
		print(name)
		print(url.split("/")[-1])
		print(url)
		command = ['fbdown.py', url]
		subprocess.call(command, shell=True)
		#fbdown.main(url, item.storage_location)

		
		for f in os.listdir(item.storage_location):
			if not f.endswith(".mp4"):
				src = os.path.join(item.storage_location, f)
				dst = os.path.join(item.storage_location, f+".mp4")
				os.rename(src, dst)

		os.chdir(cwd)
		item.completed = True
		if os.listdir(item.storage_location)==[]:
			item.completed = False
	except Exception as e:
		print(str(e))
		os.chdir(cwd)
		item.completed = False
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

def get_videos(item):

	"""Gets list of video links and then downloads each video. Set item.flag = True if complete."""
	
	print(item.id)
	print("Videos")
	flag = False
	item.agent_name = agent_name+"_get_videos"
	driver = webdriver.Firefox()
	print("here0")
	try:
		cwd = os.getcwd()
		print("here1")
		if not os.path.exists(item.storage_folder):
			os.makedirs(item.storage_folder)
		downloaded_files = os.listdir(item.storage_folder)
		print("here2S")
		driver.set_window_size(768,1024)
		driver.get(item.url)
		driver.maximize_window()
		sleep(2)
		try:
			login_button = driver.find_element_by_tag_name("a").click()
		except:
			button_flag = False
			login_button = driver.find_elements_by_tag_name('a')
			for el in login_button:
				if not button_flag:
					if "login" in el.get_attribute("href"):
						el.click()
						button_flag = True
		print("here6")
		driver.find_element_by_id("email").send_keys(facebook_login)
		driver.find_element_by_id("pass").send_keys(facebook_password)
		login_button = driver.find_element_by_tag_name("form").submit()
		sleep(5)
		print("here3")
		driver.get(item.url)
		print("here4")
		sleep(5)
		scroll_down(driver)
		my_links = []
		my_links_dict = {}
		print("here5")
		soup = bs(driver.page_source, 'lxml')
		entries = soup.select('.entry-title > a')
		links  = soup.find_all("a",href=True)

		print(len(links))
		for link in links:
			if "videos" in link.attrs["href"]:
				title = ""
				try:
					title_span = link.find_all("span")#[0].find_all("span")[0].get_text
					if len(title_span)==2:
						print("here6")
						title = title_span[1].text
						print(title)
				except Exception as e:
					print(str(e))
				if not link.attrs["href"] in my_links:
					my_links.append(link.attrs["href"])
				if title!="" and not link.attrs["href"] in my_links_dict.keys():
					my_links_dict[link.attrs["href"]]=title
		os.chdir(item.storage_folder)
		metadata_file = "metadata"+dt.now().strftime("_%d_%m_%Y")+".json"
		with open(metadata_file,'w') as json_file:
			json.dump(my_links_dict, json_file)
		print("here7")
		print(len(my_links))
		print(len(my_links_dict))
		for i,link in enumerate(my_links):
			print(link)
			# if "?" in link:
			# 	link = link.split("?")[0]
			sleep(5)
			title = ""
			video_id = link.rstrip("/").split("/")[-1]
			print(downloaded_files)
			#print(link)
			print("here8")
			print(video_id+".mp4")
			#my_path = os.path.join(item.storage_folder, video_id, video_id+".mp4")
			print(os.getcwd())
			if not video_id+".mp4"  in downloaded_files:
				
				command = ['python',r'C:\Source\fbdown.py', link]#"--output", my_path]
				try:
					subprocess.call(command, shell=True)
				except Exception as e:
					print(str(e))
					if os.path.isfile(video_id+".mp4"):
						os.remove(video_id+".mp4")
						try:
							if os.path.isfile(video_id+".mp4"):
								os.remove(video_id+".mp4")
							subprocess.call(command, shell=True)
						except Exception as e:
							print(str(e))
							with open("errors.txt","a") as f:
								f.write(link)

				with open("links_processed.txt","a") as f:
					f.write(link)
					f.write("\n")
				if i==len(my_links)-1:
					flag = True
		os.chdir(cwd)
		item.completed = flag

	except Exception as e:
		print(str(e))
		os.chdir(cwd)
		item.completed = False
	print(item.completed)
	return item

