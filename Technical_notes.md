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
        column [m] ("Collected (Y/N)") 	set to "Y"
    else:
        column [m] ("Collected (Y/N)") 	set to "N"
    
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

## facebook_harvesters.py

At version `facebook_harvesters_1`
