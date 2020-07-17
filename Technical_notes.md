# Technical Notes

## Summary

This tool has two main parts: the Harvest Manager, and content harvesters focused on different types of social media content.

It is designed to be modular, and extensible. Any harvester can be changed without impacting the rest of the tool. New harvesters can be added without major changes being needed. A suitable ContentType string needs to be added to the Google sheet, and also to the [`my_content_types_master.txt`](https://github.com/jayGattusoNLNZ/harvester_manager/blob/master/my_content_types_master.txt) file in this repo. 

The harvesters use any method they can to complete an individual harvest. This can be Python native code, or a `subproc` call from within python to commandline visible tools.

The Harvest Manager is driven by the contents of an assigned Google sheet. 

It was built in a huge hurry due to emerging Covid-19 collection needs, whcih means that there is lots to go back and clean up if its expected to work as BAU tool. Only mission critical code was changed during its rapid build. This also means there will be errors and bugs. Apols.     

Written in python 3.6+

# The Manager


Currently: `beta_2_manager.py`

### to do 

1. Abstract key management into its own function / script for better / easier management. 
2. Abstract the spreadsheet reading so the `Item` class object is built by column heading name/string, and not column ID. (Things get moved around, things get added/removed)
3. Build a spoofing/testing `item()` and testing 'spreadsheet' to mock all the harvester cases (see `main()` in `twitter_harvesters.py` for basic approach.
4. Build in way of calling any harvester independently (see `main()` in `twitter_harvesters.py` for basic approach\).
5. Fix the confusion over `self.storage_folder` and `self.storage_location` in `Item()`
6. Fix all the harvesters so they properly follow the agreed harvest content structure. This requirement was a late addition, so some earlier harvesters do not adhere to the rules. Assume any v1 harvester needs to be cleaned up. 


### Notes

Opens the Google sheet, and consumes it row by row. 

One row is converted into an item class object that is handed to the harvester (and handed back again at the end of the harvest)

The item class is an exchange object - all harvesters are built to accept and return a `Item()` object. 

The minimum `Item()` class data object for exchange with a harvester module is: 

    self.id # string 
    self.ready # bool
    self.content_type # controlled vocab
    self.url # string 
    self.date_range  # can be None
    self.scope  # contolled vocab - not currently used
    self.storage_location # not really used, see self.storage_folder
    self.completed # bool
    self.storage_folder # string
    self.agent_name # string - set in harvester
    self.archived_start_date # can be None 
    self.row_number # int - used when writing outcomes to spreadsheet after harvest

There are more fields, these drive behaviour in the Manager layer, or are informational only. 

When an `Item()` class object comes back from a harvester the following data is included in the `Item()` object:

    self.completed # bool
    self.agent_name # string
    self.completed # bool (must be True) 
    
When an `Item()` object is returned, the following fields in the spreadsheet may be updated by the Manager:
    
    column [l] = "Date Archived" # (dd/mm/yy) 
    if item.reccuring == "N":
        column [m] ("Collected (Y/N)") is set to "Y"
    else:
        column [m] ("Collected (Y/N)") is set to "N"
    
    column [n] 'Staff/Team Responsible' set to item.agent_name
    column [o] 'Storage Location' set to item.storage_folder)

# Harvesters

All harvesters have to follow the same pattern:

1. Must accept a properly populated `Item()` class object as the input; returns the same object with extra data 
2. Must have an agent name
3. Agent names must be incremented at version change so it's clear which version was used at any time
4. Must be able to 'see' (write to) the storage location
5. Must accept the `item.url` as the primary seed
6. On success, return `item.completed` as `True`
7. On failure, return `item.completed` as `False`
8. The harvester does not touch (read or write) the Google sheet
9. Individual harvester's methods are self contained python functions
10. Harvester functions related by platform  (TwitterTweet, TwitterAccount) should be grouped in to one library, (`twitter_harvesters.py`) but called individually (`from twitter_harvesters import get_tweet as twitter_get_tweet`, `from twitter_harvesters import get_account as twitter_get_account`) 
11. Harvester functions can be called anything sensible in the library, but aliased into the Manager via the following convention: `[platform]_get_[unit]` 
12. All harvested content adheres to the agreed harvested content structure.  

## Harvested Content Structure

The storage location for any content must be carefully chosen. 

Be aware of overwriting any content if items are harvested repeatedly. 
Be aware of moving content around after harvest - use archivally 'safe' moving tools like rsync, collection harmoniser (https://github.com/jayGattusoNLNZ/files_harmoniser), or safemover (https://github.com/NLNZDigitalPreservation/Safe_mover). 
Be aware of the volume you might collect. These tools can collect large volumes of data - make sure you have sufficent local / final storage. 

The structure of harvested content should follow this pattern:

1. The root folder for any harvest is the unique ID listed on the shared Google sheet, e.g.  `.\1000991\`
    It is the job of the harvester to make this folder. 
2. There is always at least one child folder which is another unique ID. This should come from the content source. e.g. if the unit being harevsted is a YouTube video, there is child folder that is the labelled the YouTube video ID. e.g.  `.\1000991\tehEEHS23\`
3. If there are mutiple items (e.g. a YouTube playlist) there are multiple child folders with each content ID as its label.  e.g.  `.\1000991\tehEEHS23\`, `.\1000991\erhfrYYHe7\`, `.\1000991\aebbdfYYG734\` etc.  
3. Inside this folder is all content that relates to the harvested item, including things like comments and other metadata. 
4. Any content that isn't epected to change (e.g. the YouTube video, or the Instagram image) is placed here, and has the ID as its filename, with an approriate file extension.    e.g. `.\1000991\tehEEHS23\tehEEHS23.mp4`
5. Any additional content collected as part of an item harvest is placed in the child folder, and sensibly labelled. Pay attention to repeated harvests, and how items contents like 'comments' or informational blocks like a "tweet" may change. Use a combination of item ID, a hint keyword, and datetime stamp in filenames to ensure that no item is accidentally over written. e.g.  `.\1000991\tehEEHS23\tehEEHS23_comments_dd-mm-yyyy.json` or `.\1000991\tehEEHS23\tehEEHS23_errors_dd-mm-yyyy.log`
This also massively helps deduping.

## The harvesters
[Facebook](#facebook_harvesterspy)  
[Instagram](#insta_harvesterspy)  
[TikTok](#tiktok_harvesterspy)  
[Twitter](#twitter_harvesterspy)  
[Vimeo](#vimeo_harvesterspy)  
[YouTube](#youtube_harvesterspy)  

### facebook_harvesters.py

At version `facebook_harvesters_1`

!todo put harvested videos in proper content structure  
!todo automate and include manual method for `get_videos` using account name as trigger URL


Currently only has only one harvester, for Facebook videos

`get_video(item)`

Takes the the `item.url` and hands it to the `fbdown` tool in commandline via `subproc`

Scope notes - Only harvests the video at a specific URL. #todo - check the products. 

If multiple videos are requested (i.e. the user wants to collect multiple videos from an account), this must be called mutiple times. 

N.B. There is a manual method for getting all the video URLs from an account. In a browser, open the Facebook page for the video feeds, manually scroll until the date range of videos required is visible in the browser. Save this browser page as an HTML file. Use the included facebook_video_url_parser.py file to get a list of video URLs. Feed them to the same process. This isn't included in the harvester as a method yet because of the manual step needed to surface the URL's HTML.  See https://github.com/jayGattusoNLNZ/harvester_manager/blob/master/work_in_progress/manual_method_for_facebook_video.py

### insta_harvesters.py

At version `insta_harvesters_1`

!todo put harvested videos in proper content structure for both harvesters 
!todo add in the comments/caption harvester - code exists [here] - needs blending in and structure agreed. 
!todo needs a get_item method.

`get_line(item)`

Takes the the `item.url` and hands it to the `pyinstalive` tool in commandline via `subproc`

`pyinstalive` live has a config file that needs to setting up with Instagram keys etc. (see https://github.com/dvingerh/PyInstaLive) 

Scope notes - collects any 'live' video thats visible on account. Live videos are visible for 24 hours. Scope is therefore any account URL, (from harvest time in spreadsheet minus 24 hours) to (harvest time in spreadsheet). Also can run as a daemon - listening/watching an account - and capture any livestreams in real time. 
Also captures comments as a text file thats part of the harvest. 

If multiple videos are found as part of the 24 hour stream archive, it collects mutiple video files.

`get_account(item)`

Takes the the `item.url` and hands it to the `instagram-scraper` tool in commandline via `subproc`

`instagram-scraper` needs an Instagram username and password - this is handled as a local instance of the normal secrets method (see [secrets_method.md](https://github.com/jayGattusoNLNZ/harvester_manager/blob/master/secrets_method.md)) in the Harvester. See https://github.com/arc298/instagram-scraper for the tool. 

It writes its own log file, which I believe it uses to handle recurrent harvesting. 

!todo need to really think about how to handle the harvester product vs the library-shaped/SIP structured content, and how to not keep reharvesting the same accounts.  

Scope notes - harvests anything visible to the given account (any public posts - video and images. Will collect whole account. 

!todo needs caption code change  - see instagram_comments_and_caption__splitter.py
!todo - cull harvest between scope dates. As last modified dates are maintained, use these as filter for date scope.  

### tiktok_harvesters.py

At version: `tiktok_harvesters_1`

!todo put harvested videos in proper content structure
!todo make get_account harvester  - manual method exists, not implemented. 

Scope notes - harvests given video URL only. 

Harvester takes given video URL, resolves the URL, finds the video object URL in resulting HTML, downloads that URL.

Manual account harvesting method exists as proof of concept: resolve account page, scroll until new thumbnails stop. Save HTML, search for video page URLs, send to get_video. Not close to implementation.  

### twitter_harvesters.py 

at version `Twitter_harvester` + sub harvester string

!todo put harvested tweets in proper content structure
!todo media resolve and save code to all harvesters in proper structure - code exists in module:  `get_assets(tweet, storage_folder)`

Uses the `twarc` tool in python to handle tweets: https://github.com/DocNow/twarc. Needs Twitter keys and setup. 

`get_tweet(item)`

At version: `Twitter_harvester_1_get_tweet`

Scope notes - takes tweet ID  as twitter URL, resolves tweet, saves tweet as json `{tweet_id}_{datetime}.json`. Does not collect any replies, etc.
!todo add in getting replies. 

Tries to find any media in the tweet and deal with it accordingly.
See `get_assets(tweet, storage_folder)`

`get_account(item)`

At version: `Twitter_harvester_1_get_account`

Scope notes - takes tweet account as URL, resolves all visible tweets, filters tweets to include only those after start date (`item.date_range` in given form from Google sheet, dd.mm.yyyy), saves tweets as json `{tweet_id}_{datetime}.json`. 
Does not collect any replies, etc.
!todo add in getting replies. 

Tries to find any media in the tweet and deal with it accordingly.
See `get_assets(tweet, storage_folder)`

`get_assets(tweet, storage_folder)`

See code for full logic. 

For a given tweet ID, checks the ['entities'] for a ['media'] section. If found, it looks in the ['extended_entities']['media']['type'] element and collects any item that is ['photo'] or ['animated_gif'] or ['video'].

Any other type is logged as a URL in code, printed to terminal, but not further processed.
!todo process unknown types

File save name is per URL. 
!todo - this needs to be cleaned up. Needs to use data structure better.   

N.B. Currently includes a basic `item()` mocking method in `main`. This should cleaned up, and reflected in all harvesters.  


### vimeo_harvesters.py

Uses youtube_dl from within Python. See https://pypi.org/project/youtube_dl/

`get_channel(item)`

At version: `vimeo_harvesters_get_channel`  
!todo version agent_name properly - done SK
!todo needs general clean up / code review - somehow done SK

Takes channel as URL from `item`, and scrapes all videos visible to youtube-dl (public videos). 

Scope notes - takes channel URL, uses youtube-dl to find video IDs, and checks if each video date is later than `archive_start_date`. Then downloads each video and its metadata by video ID with youtube-dl, and puts video and metadata in json format in a folder with name equal to video ID. It also creates a CSV report file at the same level as the video folders: each row contains project ID, video ID, date and "True" or "False" for metadata for each attempt. Sets `item.collected=True` if fully collected and not recurring.

`get_video(item)`

At version: `vimeo_harvesters_get_video`  
!todo version agent_name properly - done SK
!todo needs general clean up / code review 

Takes video as URL from `item`, and scrapes video if visible to youtube-dl (public videos). 

Scope notes - takes URL, gets video ID, and downloads video and metadata by video ID with youtube-dl. It puts the video and metadata in json format in a folder with a name equals to video ID. It also creates a CSV report file at the same level as the video folder: contains project ID, video ID, date and "True" or "False" for metadata for each attempt. Sets `item.collected=True` if collected.

!todo comments? 

### youtube_harvesters.py

Uses [youtube_dl](https://pypi.org/project/youtube_dl/) from within Python, the [YouTube API](https://developers.google.com/youtube/v3) for metadata and some HTML scraping with [Selenium](https://selenium-python.readthedocs.io/getting-started.html) and [ChromeDriver](https://chromedriver.chromium.org/) to get video IDs. 

Comments - Comments can be disabled or video and metadata not available for particular day and could be picked up later. 

`get_video(item)`

At version: `youtube_harvesters_get_video`  
!todo version agent_name properly  
!todo needs general clean up / code review  

Takes video as URL from `item`, and scrapes video if visible to youtube-dl (public videos). 

Scope notes - takes URL, and then downloads the video with youtube-dl and the metadata and comments with the YouTube API, puts video and metadata and comments (if any) in json format in a folder with name equal to video ID. It also creates a CSV report file at the same level as the video folder: contains project ID, video ID, date and "True" or "False" for video, metadata and comments for each attempt. Sets `item.collected=True` if collected.

`get_channel(item)`

At version: `youtube_harvesters_get_channel`  
!todo version agent_name properly  
!todo needs general clean up / code review  

Takes channel as URL from `item`, and scrapes all videos visible to youTube-dl (public videos). 

Scope notes - takes channel URL, uses YouTube API to find video IDs, and checks if each video date is later then `archive_start_date`. It then downloads each video with youtube-dl and the metadata and comments with the YouTube API, puts each video with metadata and comments (if any) in json format in a folder with name equal to video ID. It also creates a CSV report file at the same level as the video folders: each row contains project ID, video ID, date and "True" or "False" for video, metadata and comments for each attempt. Sets `item.collected=True` if fully collected and not recurring.

`get_playlist(item)`

At version: `youtube_harvesters_get_playlist`  
!todo version agent_name properly  
!todo needs general clean up / code review  

Takes playlist as URL from `item`, and scrapes all videos visible to youTube-dl (public videos). 

Scope notes - takes playlist URL, uses YouTube API to find video IDs, and checks if each video date is later then `archive_start_date`. It then downloads each video with youtube-dl and the metadata and comments with the YouTube API, puts each video with metadata and comments (if any) in json format in a folder with name equal to video ID. It also creates a CSV report file at the same level as the video folders: each row contains project ID, video ID, date and "True" or "False" for video, metadata and comments for each attempt. Sets `item.collected=True` if fully collected and not recurring.

`get_user(item)`

At version: `youtube_harvesters_get_user`  
!todo version agent_name properly  
!todo needs general clean up / code review  

Takes user as URL from `item`, and scrapes all videos visible to youTube-dl (public videos). 

Scope notes - takes user account URL, uses Selenium and ChromeDriver to find video IDs, and checks if each video date is later then `archive_start_date`. It then downloads each video with youtube-dl and the metadata and comments with the YouTube API, puts each video with metadata and comments (if any) in json format in a folder with name equal to video ID. It also creates a CSV report file at the same level as the video folders: each row contains project ID, video ID, date and "True" or "False" for video, metadata and comments for each attempt. Sets `item.collected=True` if fully collected and not recurring.
