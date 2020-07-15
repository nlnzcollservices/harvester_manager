# harvester_manager

Harvester Manager is a tool that automates the harvest of content from a variety of social platforms. 

Its designed to allow content collection staff to work autonomously, focusing on collection building.  

It was put together during the Covid19 lockdown, to help with rapid collection of the covid19 experience as expressed through social media. 

As a result, some parts of the process are underworked and have been intentionlly left in a 'just working' state. There is a developement plan included for all items in the technical_notes.md file.    
___ 

Conceptually, the tool looks a bit like this:- 

---->*Social Media Harvest Google Spreadsheet*  

Content Collectors add content to a google spreadsheet - this is specified below. 

----> Harvest manager Tool
----> (gives harvest jobs from spreadsheet to various harvester modules as needed)
-----> Currently supported: 

---------> Twitter
---------------> Tweet
---------------> Account

---------> YouTube
---------------> Video
---------------> Playlist
---------------> User
---------------> Channel

--------->  Instagram
---------------> Live videos
---------------> Account 

---------> Tiktok
---------------> Video

---------> Vimeo
---------------> Account
---------------> Video

---------> Facebook
---------------> Video

The manager tool is responsible for handing out harvest jobs (from various platforms) to a suitable harvester, and tracking the the outcomes on a shared spreadsheet  

## The harvest manager

The harvester manager, when run, pulls the sheet from googledocs and row by row checks if it needs to do anything. 

#### Choice one - do nothing

this condition is met when:

Column D (Ready for harvest) is set to `N` or `?`
or 
Column M (Collected) is set to `Y`
or 
Column M (Collected) is set to `Y` and column J (Recurring) is set to `Y`

The '?' indicator was used by techncial operators when they couldn't harvest an item that had been set to 'Y'. It typcially meant the human collector needed to check the url. 

!todo - some of the logic here is iffy in the codebase. The notion of recurring is not well handled at the moment.  

#### Choice two - atttempt harvest

If none of the conditions for do nothing are met, the tool them checks to see if its expecting to collect that particular content type. 
It does this by comparing the value found in column D (Content type) and the items listed in the file called `my_content_types.txt`

If it can find a corresponding string, it initiates the appropriate harvester module. Otherwise it does nothing. 

This is so different machines can be set up to only capture specific content depending on the team setup. 

## The harvesters

The spreadsheet row data is handed off to the appropriate harvester. Each harevster is documented below - see the technical readme for more notes / scoping paramaters (if any). 

See `Technical_notes.md` for more details and developement plans/bugs

Upon successful harvest, the resulting data is put in an agreed storage location, and key information is handed back to the manager tool, who updates the google sheet as needed. 

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

You need a google docs api key/credentials. These are managed in script as local variables via the usual secrets method. 

### column a - 'Unique Identifier'

Originally the tool was designed to support multiple assets against a single ID - conceptually allowing mutiple sources to aggregated in to a single folder. It was a terrible idea. Do not reuse unique identifiers :( 

This is used as the parent folder for any content collected for this row

### column b - 'Brief Description'

Describes identified content 

Used by curatorial staff. 

### column c - 'Creator (if known)'

Name of content creator

Used by curatorial staff

### column d - 'Ready for harvest (Y/N/?)'

Accepts only `Y`, `N` or `?`

`?` is used by technical staff to indicate they had a problem with the content and need the owner to check it. 

### column e - 'Category'

Type of content. Useful for ntoing collection destination.  

Used by curatorial staff

### column f - 'Location'

Not used. 

Content platform. 

### column g - 'Content Type (list)'

Used to steer the harvester choice by the manager tool. Choices are sub platform (e.g. TwitterAccount, or TwitterTweet). Each choice has a matching harvester function that does the work.  

The list of mostly working harvesters is found in the `my_content_types_master.txt` in the git. 

    FacebookVideo
    InstagramAccount
    InstagramItem
    InstagramLive
    TiktokVideo
    TwitterTweet
    TwitterAccount
    VimeoVideo
    YoutubePlaylist
    YoutubeChannel
    YoutubeUser
    YoutubeVideo
    TwitchVideo
    TwitchAccount
    VimeoVideo
    VimeoChannel

Each manager instance has its own list of harvesters it supports, as specified in the file `my_content_types.txt` This file should be changed to ensure that each manager instance only harvests content the host machine is set up for, or as suits a division of labour. This means that many managers can be set up to work in one shared spreadsheet 

NB. This list was originally designed to hold only havesters that have a working method. This become tricky to maintain as the project grew, and as such, there are content types that do not yet have working harvesters:

    InstagramItem
    TwitchAccount

### column h - 'Link'

This is the triggering URL. The start of any harvest. Has to be correct for the content type selected. Technical details, especially around URL selection and subsequent harvest scope are found in the tehcnical read me in this git.  

### column i - 'Date range'

Used to describe if the whole account is grabbed, or jsut a range. 

Not properly implimented yet :( 

### column j - 'Recurring (Y/N)' 

Used to say if there is an expectation that this account is regularly harvested. 

Not well implemented

### column k - 'Scope'

describes the atomic data types expected. 

Currently only informational. It was intended to describe the desirable scope of the harvest, and eventually to drive any scoping behaviour to set out 'depth' of harvest. 

### column l - 'Date Archived'

Written by harvester when completed. 

### column M - 'Collected (Y/N)'

Set by harvester when completed

### column N - 'Staff/Team Responsible'

Records the last hand to touch the item.

Written manually or by the harvester - if the havester is doing the setting, the data is collected from a version string recorded in the harvester code. 

### column o - 'Storage Location'

Records the location of the harvest. Complicated when stuff is on different machines or moved after the fact.

The whole tool uses the unique ID as folder label for any content collected - so this location should really tell us what the root folders are for the harvest ID folder, and  
what machine the harvest is on. Needs some clean up work. #todo


### column p - 'Notes'

Human notes. 

### column q - 'Screengrabs (Y/N)'

Not used yet. The intent is to add in another screen shotting tool, and support the making of a screen grab image of a url to augment a harvest. The screen shotter code exists here: https://github.com/jayGattusoNLNZ/page_harvester but has not been built into the struture of this project yet.  
