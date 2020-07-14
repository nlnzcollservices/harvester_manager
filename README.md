# harvester_manager

The codebase that runs the social media harvester manager. 

Collectors add content to a google spreadsheet - this is specified below. 

The manager tool is responsible for handing out harvest jobs (from various platforms) to a suitable harvester, and tracking the the outcomes on a shared spreadsheet  

## The harvest manager

The harvester manager, when run, pulls the sheet and row by row checks if it needs to do anything. 

#### Choice one - do nothing

this condition is met when:

Column D (Ready for harvest) is set to `N` or `?`
or 
Column M (Collected) is set to `Y`
or 
Column M (Collected) is set to `Y` and column J (Recurring) is set to `Y`

[to do - some of the logic here is iffy in the codebase]. 

#### Choice two - atttempt harvest

If none of the conditions for do nothing are met, the tool them checks to see if its expecting to collect that particular content type. 
It does this by comparing the value found in column D (Content type) and the items listed in the file called `my_content_types.txt`

If it can find a corresponding string, it initiates the appropriate harvester module. Otherwise it does nothing. 

This is so different machines can be set up to only capture specific content depending on the team setup. 

## The harvesters

The spreadsheet row data is handed off to the appropriate harvester. Each one is documented below - see the technical readme for more notes / scoping paramaters (if any). 

Upon successful harvest, the resulting data is put in an agreed location, and key information is handed back to the manager tool, who updates the google sheet as needed. 

### facebook_harvesters.py

Only handles facebook live video. If multiple videos are wanted, its best to run a custom harvest and hand off a list of video URLS. 

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



## The Spreadsheet

This is a brittle beast. The columns are hard coded. There are nuances that emerged over time. 

You need a google docs api key/credentials. These are managed in script as local vars. 

### a - Unique Identifier

Originally the tool was designed to support multiple assets against a single ID - conceptually allowing mutiple sources to aggregated in to a single folder. It was a terrible idea. Do not reuse unique identifiers :( 

This is used as the parent folder for any content collected for this row

### b - Brief Description

Describes identified content 

Used by curatorial staff. 

### c - Creator (if known)

Name of content creator

Used by curatorial staff

### d - Ready for harvest (Y/N/?)

Accepts only `Y`, `N` or `?`

`?` is used by technical staff to indicate they had a problem with the content and need the owner to check it. 

### e - Category

Type of content. Useful for ntoing collection destination.  

Used by curatorial staff

### f - Location

Not used. 

Content platform. 

### g - Content Type (list)

Used to steer the harevster choice. Choices are sub platform (e.g. TwitterAccount, or TwitterTweet) 

### h - Link

This is the magical URL. the start of any harvest. 

### i - Date range

Used to describe if the whole account is grabbed, or jsut a range. 

Not properly implimented yet :( 

### j - Recurring (Y/N) 

Used to say if there is an expectation that this account is regularly harvested. 

Not well implemented

### k - Scope

describes the atomic data types expected. 

Currently only informational. 

### l - Date Archived

Written by harvester when completed. 

### M - Collected (Y/N)

Set by harvester when completed

### N - Staff/Team Responsible

Tries to record the last hand to touch the item. 
Written manually or by the harvester

### o - Storage Location

Tries to record the location of the harvest. Complicated when stuff is on differnet mahcines or moved... 

### p - Notes

Human notes. 


### q - Screengrabs (Y/N)

Not used yet. 
