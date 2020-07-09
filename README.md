# harvester_manager

The codebase that runs the social media harvester manager. 

# The project

Collectors add content to a google spreadsheet. 
The harvester manager, when run, pulls the sheet, and row by row checks if it needs to do anything. 

### Choice one - do nothing

this condition is met when:

Column D (Ready for harvest) is set to `N` or `?`
or 
Column M (Collected) is set to `Y`
or 
Column M (Collected) is set to `Y` and column J (Recurring) is set to `Y`

[to do - some of the logic here is iffy in the codebase]. 

### Choice two - atttempt harvest

If none of the conditions for do nothing are met, the tool them checks to see if its expecting to collect that particular content type. 
It does this by comparing the value found in column D (Content type) and the items listed in the file called `my_content_types.txt`

If it can find a corresponding string, it initiates the appropriate harvester module. Otherwise it does nothing. 

This is so different machines can be set up to only capture specific content depending on the team setup. 

## The harvest

The spreadsheet row data is handed off to the apporiate harvester. Each one will be documented below. 

Upon success, the resulting data is handed back to the manager script, who updates the google sheet as needed. 

### facebook_harvesters.py

Only handles facebook live video. If multiple videos are wanted, its best to run a custom harvest and had off a list of video URLS. 

Requires the `fbdown` tool to be accessible to the calling machine commandline

https://pydoc.net/fb-down/1.0.1/fbdown/

### insta_harvesters

has two modes, and needs two tools 

1.

`pip3 install pyinstalive`

https://github.com/dvingerh/PyInstaLive

and 

2. 

`pip3 install instagram-scraper`

https://github.com/rarcega/instagram-scraper

### tiktok_harvesters

Uses standard python libs :) 

### twitter_harvesters

Needs twarc set up properly. (needs keys and all sorts). 
https://github.com/DocNow/twarc


### vimeo_harvesters

Needs youtube-dl at commandline 

https://ytdl-org.github.io/youtube-dl/index.html


### youtube_harvesters

Needs youtube-dl at commandline 

https://ytdl-org.github.io/youtube-dl/index.html

