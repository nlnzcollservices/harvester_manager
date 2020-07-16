import json
import os
import shutil
import simplejson
import hashlib
from copy import deepcopy

"""
This is a working test of the splitting up of harvested instagram account (not live) json to surface comments chunks and item captions. 

It needs a change to the insta harvester - it needs the addtional CLI tag -T= to capture the json file.  

It needs cleaning up. 

The output data shape needs agreeing with content collectors. 

It needs blending into to the existing code base properly, and then needs re-running over the harvested instagram accounts.   

"""

# this is where the harvested files are 
local_file_store = r"C:\projects\misc_harvesters\insta_comments\test\jacindaardern"

# this is the also harvested instagram comments file. 
my_file = r"C:\projects\misc_harvesters\insta_comments\test\jacindaardern\jacindaardern.json"

# this is where the spilt up items will be put. 
item_storage_location_root = r"items" 

if not os.path.exists(item_storage_location_root):
	os.makedirs(item_storage_location_root)


def get_list_files_in_folder(my_folder):
	return os.listdir(my_folder)

def check_harvested_vs_moved(found_content):
	"""
	Checking service that makes sure all harvested items got processed and copied. 
	"""
	harvested_content = get_list_files_in_folder(local_file_store)
	print ()
	print ("Number of found items that got moved:", len(found_content))
	print ("Number of items that got harvest initially:", len(harvested_content))
	for item in harvested_content:
		if item not in found_content:
			print ("Didn't find a folder for:", item)
	print ()

def get_get_json_from_file(my_file):
	"""
	Take a json file, returns a json object
	"""
	with open(my_file, encoding="utf8") as data:
		text = data.read()
	return simplejson.loads(text)


def process_json(my_json):

	### testing limiter - used to limit number of items its processing 
	process_limit = 100000000000000
	found_content = []

	for i, item in enumerate(my_json['GraphImages']):

		# gets the instagram item id 
		my_item_folder = os.path.join(item_storage_location_root, item['shortcode'])

		# makes a folder for that item
		if not os.path.exists(my_item_folder):
			os.makedirs(my_item_folder)

		### get all the files for each post out of the post json urls list 
		for url in item["urls"]:

			#safety check to test assumption theres always a ? in the url. 
			if "?" not in url:
				print (f"No ? found in url: {url}")
				quit()
			else:
				url, __ = url.split("?", 1)

			__, content_file_name = url.rsplit("/", 1) 
			found_content.append(content_file_name)
			local_content_path = os.path.join(local_file_store, content_file_name)

			#checks for harvested item in harvest store, and copies it into the new item folder
			if not os.path.exists(local_content_path):
				print (f"File not found: {local_content_path}")
				quit()
			else:
				dst = os.path.join(my_item_folder, content_file_name )
				if not os.path.exists(dst):
					shutil.copy2(local_content_path, dst)
		#########

		### make individual json and put in item folder
		json_filename = item['shortcode']+".json"
		item_json_path = os.path.join(my_item_folder, json_filename)
		if not os.path.exists(item_json_path):
			with open(item_json_path, "w") as outfile:
				outfile.write(json.dumps(item,sort_keys=True,indent=4,separators=(',', ': ')))

		json_filename = item['shortcode']+"_no_comments.json"
		item_no_comments_json_path = os.path.join(my_item_folder, json_filename)
		if True:
			with open(item_no_comments_json_path, "w") as outfile:
				temp_item = deepcopy(item)
				temp_item['comments']['data'] = []
				outfile.write(json.dumps(temp_item,sort_keys=True,indent=4,separators=(',', ': ')))	
		######

		##### make comments file #####
		comments = []
		json_filename = item['shortcode']+"comments_only.json"
		comments_json_path = os.path.join(my_item_folder, json_filename) 
		for comment in item['comments']['data']:
			comments.append(comment)
		with open(comments_json_path, "w") as outfile:
			comments_item = {"comments":comments}
			outfile.write(json.dumps(comments_item,sort_keys=True,indent=4,separators=(',', ': ')))
		######

		##### make comments file - with redacted user IDs #####
		comments = []
		json_filename = item['shortcode']+"comments_only_IDs_redacted.json"
		comments_json_path = os.path.join(my_item_folder, json_filename) 
		for comment in item['comments']['data']:
			comment["id"] = hashlib.md5(comment["id"].encode()).hexdigest()
			comment["owner"]["id"] = hashlib.md5(comment["owner"]["id"].encode()).hexdigest()
			comment["owner"]["username"] = hashlib.md5(comment["owner"]["username"].encode()).hexdigest()
			comment["owner"]["profile_pic_url"] = hashlib.md5(comment["owner"]["profile_pic_url"] .encode()).hexdigest()
			cleaned_text = []
			for word in comment["text"].split(" "):
				if word.startswith("@"):
					cleaned_text.append("@"+hashlib.md5(word.encode()).hexdigest())
				else:	
					cleaned_text.append(word)
			comment["text"] = " ".join(cleaned_text)
			comments.append(comment)
		with open(comments_json_path, "w") as outfile:
			comments_item = {"comments":comments}
			outfile.write(json.dumps(comments_item,sort_keys=True,indent=4,separators=(',', ': ')))
		#####


		print (item["shortcode"])

		if i == process_limit:
			print (f"reached limit: {process_limit}")
			quit()

	return found_content



my_json = get_get_json_from_file (my_file)
found_content = process_json(my_json)

check_harvested_vs_moved(found_content)

