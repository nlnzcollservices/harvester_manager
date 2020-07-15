# Technical Notes

## Summary

This tool has two main parts. A harvest manager, and content harvesters.

Its designed to be modular, and extensible. Any harvester can be changed without impacting the rest of the tool. New harvesters can be added without 

The harvesters use any method they can to do an individual harvest. This can be python native code, or a `subproc` call from within python to any commandline visible tool

The manager is driven by the contents of an assigned google spreadsheet. 

It was built in a huge hurry due to emerging covid19 collection needs, whcih means that there is lots to go back and clean up if its expected to work as BAU tool. Only mission critical code was changed during its rapid build. This also means there will be errors and bugs. Apols.     

Written in python 3.6+

# The Manager


Currently: `beta_2_manager.py`

### to do 

1. Abstract key management into its own function / script for better / easier management. 
2. Abstract the spreadsheet reading so the `Item` class object is built by column heading name/string, and not column ID. (Things get moved around, things get added/removed)
3. Build a spoofing/testing `item()` and testing 'spreadsheet' to mock all the harvester cases (see `main()` in `twitter_harvesters.py` for basic approach.
4. Build in way of calling any harvester independently (see `main()` in `twitter_harvesters.py` for basic approach.
5. Fix the confusion over `self.storage_folder` and `self.storage_location` in `Item()`
6. Fix all the harvesters so they properly follow the agreed harvest content structure. This requirement was a late addition, so some earlier harvesters do not adhere to the rules. Assume any v1 harvester needs to be cleaned up. 


### Notes

Opens the sheet, and consumes it row by row. 

One row is converted into an item class object that is handed to the harvester. (And handed back again at the end of the harvest)

The item class is exchange object - all harvesters are built to accept and return a `Item()` object. 

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

There are more fields, these drive behaviour in the manager layer, or are informational only. 

When an `Item()` class object comes back from a harvester the following data is needed in the `Item()` object:

    self.completed # bool
    self.agent_name # string
    self.completed # bool (must be True) 
    
When an `Item()` object is returned, the following fields in the spreadsheet may be updated:
    
    column [l] = "Date Archived" # (dd/mm/yy) 
    if item.reccuring == "N":
        column [m] ("Collected (Y/N)") is set to "Y"
    else:
        column [m] ("Collected (Y/N)") is set to "N"
    
    column [n] 'Staff/Team Responsible' set to item.agent_name
    column [o] 'Storage Location' set to item.storage_folder)

# Harvesters

All havesters have to follow the same pattern. 

1. Must accept a properly populated `Item()` class object as the input, returns the same object with extra data at completetion. 
2. Must have an agent name
3. Agent names must be incremented at version change so its clear which version was used at any time
4. Must be able to 'see' (write to) the storage location
5. Must accept the `item.url` as the primary seed. 
6. On success return `item.completed` as `True`
7. On failure return `item.completed` as `False`
8. The harvester does not touch (read or write) the spreadsheet
9. Individual harvesters methods are self contained python functions
10. Harvester functions related by platform  (TwitterTweet, TwitterAccount) should be grouped in to one library, (`twitter_harvesters.py`) but called individually  (`from twitter_harvesters import get_tweet as twitter_get_tweet`, `from twitter_harvesters import get_account as twitter_get_account`) 
11. Harvester functions can be called anything sensible in the libary, but aliased into the manager via the following convention `[platform]_get_[unit]` 
12. All havested content adheres to the agreeed harvested content structure.  

## Harvested Content Structure

The storage location for any content must be carefully chosen. 

Be aware of overwriting any content if items are harvested repeatedly. 
Be aware of moving content around after harvest - use archivally 'safe' moving tools like rsync, collection harmoniser (https://github.com/jayGattusoNLNZ/files_harmoniser), or safemover (https://github.com/NLNZDigitalPreservation/Safe_mover). 
Be aware of the volume you might collect. These tools can collect large volumes of data - make sure you have sufficent local / final storage. 

The structure of harvested content should follow this pattern. 

1. The root folder for any harvest is the unique ID listed on the shared spreadsheet. 
    e.g.  `.\1000991\`
    It is the job of the harvester to make this folder. 
2. There is always at least one child folder which is another unique id. This should come from the content source. e.g. if the unit being harevsted is a youtube video, there is child folder that is the labelled the youtube video ID. e.g.  `.\1000991\tehEEHS23\`
3. If there are mutiple items (e.g. a youtube playlist) there are multiple child folders with each content ID as its label.  e.g.  `.\1000991\tehEEHS23\`, `.\1000991\erhfrYYHe7\`, `.\1000991\aebbdfYYG734\` etc.  
3. Inside this folder is all content that relates to the harvested item. 
4. Any content that isn't epected to change (e.g. the youtube video, or the instaagram image) is placed here, and has the id as its filename, with an approriate file extension.    e.g. `.\1000991\tehEEHS23\tehEEHS23.mp4`
5. Any additional content collected as part of an item harvest is placed in the child folder, and sensible labelled. Pay attention to repeated harvests, and how items contents like 'comments' or informational blocks like a "tweet" may change. Use a combination of item ID, a hint keyword, and datetime stamp in filenames to ensure that no item is accidentally over written. e.g.  `.\1000991\tehEEHS23\tehEEHS23_comments_dd-mm-yyyy.json` or `.\1000991\tehEEHS23\tehEEHS23_errors_dd-mm-yyyy.log`
This also massively helps deduping.


## facebook_harvesters.py

At version `facebook_harvesters_1`

!todo put harvested videos in proper content structure
!todo automate and include manual method for `get_videos` using account name as trigger URL


Has only one harevster for live videos

`get_video(item)`

Takes the the `item.url` and hands it to the `fbdown` tool in commandline via `subproc`

Scope notes - Only harvests the given URL. #todo - check the products. 

If multiple videos are requested, this must be called mutiple times. 

N.B. There is a manual method for getting all the video urls from an account. In a browser, open the facebook page for the video feeds, manually scroll until the date range of videos required is visible in the browser. Save this browser page as an HTML file. Use the included facebook_video_url_parser.py file to get a list of video urls. Feed them to the same process. This isn't included in the harvester as a method yet because of the manual step needed to surface the urls html.  

## insta_harvesters.py

At version `insta_harvesters_1`

!todo put harvested videos in proper content structure for both harvesters 
!todo add in the comments/caption harvester - code exists [here] - needs blending in and structure agreed. 
!todo needs a get_item method.

`get_line(item)`

Takes the the `item.url` and hands it to the `pyinstalive` tool in commandline via `subproc`

`pyinstalive` live has a config file that needs to setting up with instgram keys etc. (see https://github.com/dvingerh/PyInstaLive) 

Scope notes - collects any 'live' video thats visible on account. Live videos are visible for 24hours. Scope is therefore any account url, (from harvest time in spreadsheet minus 24 hours) to (harvest time in spreadsheet). Also can run as a daemon - listening/watching an account - and capture any live streams real time. 
Also captures comments as a text file thats part of the harvest. 

If multiple videos are found as part of the 24 hour stream archive it collects mutiple video files.

`get_account(item)`

Takes the the `item.url` and hands it to the `instagram-scraper` tool in commandline via `subproc`

`instagram-scraper` needs a instgram username and password - this is handled as a local instance of the normal secrets method in the harvester. See https://github.com/arc298/instagram-scraper

It writes its own log file, that I believe it uses to handle recurrent harvesting. 

!todo need to really think about how to handle the harvester product vs the library shaped/SIP structured content, and how to not keep reharvesting the same accounts.  

Scope notes - harvests anything visible to the given account (any public posts - video and images. Will collect whole account. 

!todo needs caption code change 
!todo - cull harvest between scope dates. As last modified dates are maintined, use these to filter for date scope.  

`tiktok_harvesters.py`

At version: `tiktok_harvesters_1`

!todo put harvested videos in proper content structure
!todo make get_account harvester  - manual method exists. not implimented. 

Scope notes - harvests given video url only. 

Harvester takes given video URL, resolves the url, finds the video object url in resulting HTML, downloads that url.

Manual account method exists as proof of concept. Resolve account page, scroll until new thumbnails stop. Save html, search for video page URLs, send to get_video. Not close to implimentation.  

## twitter_harvesters.py 

at version `Twitter_harvester` + sub havester string

!todo put harvested tweets in proper content structure
!todo media resolve and save code to all harvesters in proper structure - code exists in module:  `get_assets(tweet, storage_folder)`

Uses the `twarc` tool in python to handle tweeets. https://github.com/DocNow/twarc needs twitter keys and setup. 

`get_tweet(item)`

At version: `Twitter_harvester_1_get_tweet`

Scope notes - takes tweet id  as twitter url, resolves tweet, saves tweet as json `{tweet_id}_{datetime}.json`. Does not collect any replies etc
!todo add in getting replies. 

Tries to find any media in the tweet and deal with it accordingly
See `get_assets(tweet, storage_folder)`

`get_account(item)`

At version: `Twitter_harvester_1_get_account`

Scope notes - takes tweet account as url, resolves all visible tweets, filters tweets to include only those after start date (`item.date_range` in given form from spreadsheet, dd.mm.yyyy), saves tweets as json `{tweet_id}_{datetime}.json`. 
Does not collect any replies etc
!todo add in getting replies. 

Tries to find any media in the tweet and deal with it accordingly
See `get_assets(tweet, storage_folder)`

`get_assets(tweet, storage_folder)`

See code for full logic. 

For a given tweeeti checks the ['entities'] for a ['media'] section. If found it looks in the ['extended_entities']['media']['type'] element and collects any item that is ['photo'] or ['animated_gif'] or ['video']

Any other type is logged as a URL in code, printed to terminal, but not further processed.
!todo process unknown types

File save name is per URL. 
!todo - this needs to be cleaned up. needs to use data structure better.   

N.B. Currently includes a basic `item()` mocking method in `main`. This should cleaned up, and reflected in all harvesters.  


`vimeo_harvesters.py`

Uses youtube_dl from within python. See https://pypi.org/project/youtube_dl/

`get_channel(item)`

At version: "vimeo_harvesters_get_channel" 
!todo version agent_name properly
!todo needs general clean up / code review 

Takes channel as URL from `item`, and scrapes all videos visible to youTube-dl (public videos). 

Scope notes - !todo

`get_video(item)`

At version: "vimeo_harvesters_get_video" 
!todo version agent_name properly
!todo needs general clean up / code review 

Takes video as URL from `item`, and scrapes video if visible to youTube-dl (public videos). 

Scope notes - !todo comments? 

`youtube_harvesters.py`

Uses youtube_dl from within python. See https://pypi.org/project/youtube_dl/ and some html scraping to get IDs. 


`get_video(item)`

At version: "youtube_harvesters_get_video" 
!todo version agent_name properly
!todo needs general clean up / code review 

Takes video as URL from `item`, and scrapes video if visible to youTube-dl (public videos). 

Scope notes - !todo comments? 


`get_channel(item)`

At version: "youtube_harvesters_get_channel" 
!todo version agent_name properly
!todo needs general clean up / code review 

Takes channel as URL from `item`, and scrapes all videos visible to youTube-dl (public videos). 

Scope notes - !todo comments? 

`get_playlist(item)`

At version: "youtube_harvesters_get_playlist" 
!todo version agent_name properly
!todo needs general clean up / code review 

Takes playlist as URL from `item`, and scrapes all videos visible to youTube-dl (public videos). 

Scope notes - !todo


`get_user(item)`

At version: "youtube_harvesters_get_user" 
!todo version agent_name properly
!todo needs general clean up / code review 

Takes user as URL from `item`, and scrapes all videos visible to youTube-dl (public videos). 

Scope notes - !todo comments? 
