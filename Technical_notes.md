# Technical Notes

## Summary

All writtten in python 3.6+

Has two main parts. Manager, and harvesters. 

The harvesters use any method they can to do an individual harvest. This can be python native code, or a `subproc` call from within python to any commandline visible tool

The manager is driven by the contents of an assigned google spreadsheet. 

# The Manager

beta_2_manager.py

### to do 

1. Abstract key management into its own function / script for better / easier management. 
2. Abstract the spreadsheet reading so the `Item` class object is built by column heading name/string, and not column ID. 
a. Things get moved around. 
b. Things get added/removed
3. Build a spoofing/testing `item()` and testing 'spreadsheet' to mock all the harvester cases
4. Fix the confusion over `self.storage_folder` and `self.storage_location` in `Item()`
5. Fix all the harvesters so they properly follow the agreen content structure. This was a late addition, so some ealier harvesters do not. Assume any v1 harvester needs to be cleaned up. 


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
3. If there are mutiple items (e.g. a youtube playlist) there are multiple child folders with each content ID as its label.  e.g.  `.\1000991\tehEEHS23\`, `.\1000991\erhfrYYHe7\`,\`, `.\1000991\aebbdfYYG734\` etc.  
3. Inside this folder is all content that relates to the harvested item. 
4. Any content that isn't epected to change (e.g. the youtube video, or the instaagram image) is placed here, and has the id as its filename, with an approriate file extension.    e.g. `.\1000991\tehEEHS23\tehEEHS23.mp4`
5. Any additional content collected as part of an item harvest is placed in the child folder, and sensible labelled. Pay attention to repeated harvests, and how items contents like 'comments' or informational blocks like a "tweet" may change. Use a combination of item ID, a hint keyword, and datetime stamp in filenames to ensure that no item is accidentally over written. e.g.  `.\1000991\tehEEHS23\tehEEHS23_comments_dd-mm-yyyy.json` or `.\1000991\tehEEHS23\tehEEHS23_errors_dd-mm-yyyy.log`
This also massively helps deduping.


## facebook_harvesters.py

At version `facebook_harvesters_1`
