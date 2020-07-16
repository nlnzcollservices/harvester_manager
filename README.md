# Social Media Harvest Manager

Harvester Manager is a tool that automates content harvesting from a variety of social platforms. 

It is designed to allow content collection staff to work autonomously, focusing on collection building.  

It was put together during the Aotearoa New Zealand Covid-19 lockdown, to help with rapid collection of the Covid-19 experience as expressed through social media. 

As a result, some parts of the process are underworked and have been intentionlly left in a 'just working' state. There is a development plan included for all items in the [technical_notes.md file](https://github.com/jayGattusoNLNZ/harvester_manager/blob/master/Technical_notes.md).    
___ 

Conceptually, the tool looks a bit like this:- 

## Social Media Harvest Google Spreadsheet 

Content Collectors add content to a Google spreadsheet - this is specified below. 

## Harvest Manager Tool
Hands harvest jobs from spreadsheet to various harvester modules as needed.

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
  
The manager tool is responsible for handing out harvest jobs (from various platforms) to a suitable harvester, and tracking the the outcomes on the shared Google sheet.  

### Running the Harvest Manager

When run, the Harvest Manager pulls the Google sheet and row by row checks if it needs to do anything. 

#### Choice one - do nothing

For a given row, this condition is met when:

Column D (Ready for harvest) is set to `N` or `?`  
OR  
Column M (Collected) is set to `Y`  
OR  
Column M (Collected) is set to `Y` AND column J (Recurring) is set to `Y`

The '?' indicator was used by techncial operators when they couldn't harvest an item that had been set to 'Y'. It typically meant the human collector needed to check the URL. 

- [ ] !todo - some of the logic here is iffy in the codebase. The notion of 'recurring' is not well handled at the moment.  

#### Choice two - atttempt harvest

If none of the conditions for do nothing are met, the tool then checks to see if it knows how to collect that particular content type. 
It does this by comparing the value found in column D (Content type) and the items listed in the file called `my_content_types.txt`

If it can find a corresponding string, it initiates the appropriate harvester module. Otherwise it does nothing. 

This is so different machines can be set up to only capture specific types of content depending on the team setup. 

## The Harvesters

The spreadsheet data for each row to be processed is handed off to the appropriate harvester. Each harvester is documented below - see the [technical readme](https://github.com/jayGattusoNLNZ/harvester_manager/blob/master/Technical_notes.md) for more notes / scoping parameters (if any). 

See [`Technical_notes.md`](https://github.com/jayGattusoNLNZ/harvester_manager/blob/master/Technical_notes.md) for more details and development plans/bugs

Upon successful harvest, the harvested content and metadata is put in an agreed storage location, and key information is handed back to the Harvester Manager Tool, which updates the Google sheet as needed. 

### facebook_harvesters.py

Only handles facebook live video. If multiple videos are wanted, its best to run a custom harvest and hand off a list of video URLS. 

Requires the `fbdown` tool to be accessible to the calling machine commandline: https://pydoc.net/fb-down/1.0.1/fbdown/

### insta_harvesters

Handles Instagram accounts, posts and Live events.

Has two modes, and needs two tools:

1. `pip3 install pyinstalive` https://github.com/dvingerh/PyInstaLive

and 

2. 

`pip3 install instagram-scraper` https://github.com/rarcega/instagram-scraper

### tiktok_harvesters

Handles TikTok videos

Uses standard python libs :) 

### twitter_harvesters

Needs twarc set up properly. (needs keys and all sorts): https://github.com/DocNow/twarc


### vimeo_harvesters

Needs youtube-dl at commandline: https://ytdl-org.github.io/youtube-dl/index.html


### youtube_harvesters

Needs youtube-dl at commandline: https://ytdl-org.github.io/youtube-dl/index.html



## The Spreadsheet

This is a brittle beast. The columns are hard coded, and some nuances that emerged over time were worked around rather than re-worked. 

You need Google sheets API key/credentials. These are managed in the Harvester Manager script as local variables via the usual secrets method. 

### column A - 'Unique Identifier'

This is used as the name for the parent folder for any content collected for this row.

Originally the tool was designed to support multiple assets against a single ID - conceptually allowing mutiple sources to aggregated into a single folder. It was a terrible idea. Do not reuse unique identifiers :( 

### column B - 'Brief Description'

Describes identified content (for benefit of humans).

Used by curatorial staff. 

### column C - 'Creator (if known)'

Name of content creator.

Used by curatorial staff.

### column D - 'Ready for harvest (Y/N/?)'

Accepts only `Y`, `N` or `?`

`?` is used by technical staff after a failed harvest attempt to indicate they had a problem with actioning the row and need the owner to check it. 

### column E - 'Category'

Type of content (for benefit of humans). May be useful for determining collection destination.  

Used by curatorial staff.

### column F - 'Location'

Not used. 

Content platform. This was superceded by the more specific 'Content Type' column. 

### column G - 'Content Type (list)'

Used to determine the harvester choice by the Harvest Manager tool. Each choice has a matching harvester function that does the work.  

Choices are sub platform (e.g. TwitterAccount, or TwitterTweet) as different types/levels of content on the same platform require different harvester scripts. 

The list of mostly working harvesters is found in the [`my_content_types_master.txt`](https://github.com/jayGattusoNLNZ/harvester_manager/blob/master/my_content_types_master.txt) in the git. 

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

Each manager instance has its own list of harvesters it supports, as specified in the file `my_content_types.txt` This file should be changed to ensure that each manager instance only harvests content the host machine is set up for, or as suits a division of labour. This means that many managers can be set up to work in one shared spreadsheet. 

- [ ] !todo - This list was originally designed to hold only havesters that have a working method. This become tricky to maintain as the project grew, and as such, there are content types that do not yet have working harvesters:

```
InstagramItem  
TwitchAccount
```

### column H - 'Link'

This is the root URL for a given harvest attempt. Has to match the Content Type selected. Technical details, especially around URL selection and subsequent harvest scope are found in the [technical readme](https://github.com/jayGattusoNLNZ/harvester_manager/blob/master/Technical_notes.md) in this git.  

### column I - 'Date range'

Used to describe if the whole account is grabbed, or just a sub-range. 

- [ ] !todo - Not properly implemented yet :( 

### column J - 'Recurring (Y/N)' 

Used to designate that new content at this root URL should be regularly harvested. 

- [ ] !todo - Not well implemented

### column K - 'Scope'

describes the atomic data types expected. 

- [ ] !todo - Currently only informational. It was intended to describe the desirable scope of the harvest, and eventually to drive any scoping behaviour to set out 'depth' of harvest. 

### column L - 'Date Archived'

Written by Harvester Manager when completed. 

### column M - 'Collected (Y/N)'

Set by Harvester Manager when completed, unless Recurring is set to `Y`.

### column N - 'Staff/Team Responsible'

Records the last hand to touch the item.

Written manually or by the Harvester Manager - if the Harvester sets it, the data is collected from a version string recorded in the Harvester code. 

### column O - 'Storage Location'

Records the location of the harvest. Complicated when stuff is on different machines or moved after the fact.

- [ ] !todo - The whole tool uses the unique ID as folder label for any content collected - so this location should really tell us what the root folders are for the harvest ID folder, and what machine the harvest is on. Needs some clean up work.

### column P - 'Notes'

Notes for humans. 

### column Q - 'Screengrabs (Y/N)'

- [ ] !todo - Not used yet. The intent is to add in another screen shotting tool, and support the making of a screen grab image of a URL to augment a harvest. The screen shotter code exists here: https://github.com/jayGattusoNLNZ/page_harvester but has not been built into the structure of this project yet.  
