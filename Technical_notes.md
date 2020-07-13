### Technical Notes

## Summary

All writtten in python 3.6+

Has two main parts. Manager, and harvesters. 

The harvesters use any method they can to do an individual harvest. This can be python native code, or a `subproc` call from within python to any commandline visible tool

The manager is driven by the contents of an assigned google spreadsheet. 

## To do 

1. Clean up the secrets file - there is a method of restricting keys to local machines etc. This needs cleaning up / setting up like the usual c:\sources\secrets methods, 
and the google sheet location adding. 

2. 

## The Manager

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


	ws.update_cell(item.row_number, 12, dt.now().strftime("%d.%m.%Y") )
  column [l] = "Date Archived"
    
	if item.reccuring == "N":
		column [m] ("Collected (Y/N)") 	set to "Y"
  else:
		column [m] ("Collected (Y/N)") 	set to "N"
    
	column [n] 'Staff/Team Responsible' set to item.agent_name
	column [o] 'Storage Location' set to item.storage_folder)
