from twarc import Twarc
import os
import time
import configparser
import json
import urllib
import dateparser
from datetime import datetime, timedelta
from email.utils import parsedate_tz
import configparser

secrets_and_credentials_fold = 'C:\Source\sercrets_and_credentials'
script_folder = os.getcwd()
config = configparser.ConfigParser()
config.read(os.path.join(secrets_and_credentials_fold,"secret"))

try: 
	twitter_consumer_key = config.get("social_media_harvester","twitter_consumer_key")
	twitter_consumer_secret = config.get("social_media_harvester","twitter_consumer_secret")
	twitter_access_token = config.get("social_media_harvester","twitter_access_token")
	twitter_access_token_secret = config.get("social_media_harvester","twitter_access_token_secret")
except configparser.NoOptionError:
	pass

agent_name = "Twitter_harvester"

def tweet_date_to_datetime(datestring):
	"""converts the datetime string in the tweet into a datetime object"""
	time_tuple = parsedate_tz(datestring.strip())
	dt = datetime(*time_tuple[:6])
	return dt - timedelta(seconds=time_tuple[-1])

def json_date_to_datetime(datestring):
	"""converts the datetime string in the tweet into a datetime object"""
	return datetime.strptime(datestring, '%Y-%m-%d %H:%M:%S')

def filter_tweets_by_start_date(tweets, start_date):
	if start_date == None:
		return tweets
	else:
		start_date = dateparser.parse("01.01.2018")
		filtered_tweets = []
		for tweet in tweets:
			tweet_date = tweet_date_to_datetime(tweet["created_at"])
			if tweet_date > start_date:
				filtered_tweets.append(tweet)
		return filtered_tweets

def get_tweet(item):
	"""
	takes a tweet id and uses the twarc lib to harvest it
	searches for media in the tweet - if it can find any it also tries to download that media item
	"""
	item.agent_name = agent_name+"_1_get_tweet"
	if not os.path.exists(item.storage_folder):
		os.makedirs(item.storage_folder)
	my_content_types = []
	url = item.url
	if url.endswith("/"):
		url = url[:-1]
	__, __id = url.rsplit("/", 1)
	
	t = Twarc(twitter_consumer_key, twitter_consumer_secret, twitter_access_token, twitter_access_token_secret)
	for tweet in t.hydrate([__id]):
		get_assets(tweet, item.storage_folder)
		file_path = os.path.join(item.storage_folder, "{}_{}.json".format(time.strftime("%d-%m-%Y_%H-%M-%S"), tweet['id']))
		with open(file_path, "w") as outfile:
			json.dump(tweet, outfile)
	item.completed = True
	return item



def get_account(item):
	"""
	Uses the Twarc libtrary to surface all the tweet twarc can see via a twitter username
	Searches for media in all tweets - if it can find any it also tries to download that media item
	"""
	item.agent_name = agent_name+"_1_get_account"
	if not os.path.exists(item.storage_folder):
		os.makedirs(item.storage_folder)
	t = Twarc(twitter_consumer_key, twitter_consumer_secret, twitter_access_token, twitter_access_token_secret)
	name = item.url.strip().replace("https://twitter.com/", "").replace("?", "")
	file_path = os.path.join(item.storage_folder, "{}_{}.json".format(time.strftime("%d-%m-%Y_%H-%M-%S"), name))
	if not os.path.exists(item.storage_folder):
		os.makedirs(item.storage_folder)
	tweets = []
	for tweet in t.timeline(screen_name=name):
		tweets.append(tweet)
	tweets = filter_tweets_by_start_date(tweets, item.date_range)
	for tweet in tweets:
		get_assets(tweet, item.storage_folder )
	with open(file_path, "w") as outfile:
		 json.dump(tweets, outfile)
	item.completed = True
	return item

def get_assets(tweet, storage_folder):
	"""if media in tweet returns the url strings for logging:
	tweeter, date of tweet, url of media"""
	if "media" in tweet["entities"]:
		seen_media = []
		for tweet_item in tweet["extended_entities"]["media"]:
			for_collecting = False
			if tweet_item["type"] == "photo" or tweet_item["type"] == "animated_gif":
				download_url = tweet_item["media_url"]
				for_collecting = True
			elif tweet_item["type"] == "video":
				for i, varient in enumerate(tweet_item["video_info"]["variants"]):
					if varient["content_type"] == "video/mp4" and not for_collecting:
						download_url = varient["url"]
						for_collecting = True
			else:
				print ("Unknown media type..", tweet["tweet_id"])
				download_url = tweet_item["media_url"]
			if for_collecting:
				__, name = download_url.rsplit("/", 1)
				if "?" in name:
					name, __ = name.split("?")
				if not os.path.exists(os.path.join(storage_folder, name)):
					urllib.request.urlretrieve(download_url, os.path.join(storage_folder, name))



def main():
	pass
	###example minimum item() class data object for testing 
	# item = {
	# 	"url":"https://twitter.com/ndha_nz",
	# 	"storage_folder":"./my_tweets",
	# 	"date_range":"01.03.2020"
	# 	}
	
	#### eample of how call the harvesters outside of the manager. 
	# print (item)
	# get_account(item)
	# # get_tweet(item)


if __name__ == '__main__':
	main()
