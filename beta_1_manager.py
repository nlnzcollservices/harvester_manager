import os
import gspread
import json
import sys
from oauth2client import file
from datetime import datetime as dt
import httplib2

harvester = "harvester v.2"
project_folder = "\\".join(os.getcwd().split('\\')[:-1])
sys.path.insert(0, r'H:\secrets_and_credentials')
script_folder = os.getcwd()
secrets_and_credentials_fold = r"H:\secrets_and_credentials"
sprsh = "10gH4yPpoW-JRVIIBbsKqzoa8Qz5WvZGz52lWFqC5JuQ"
credential_file = os.path.join(secrets_and_credentials_fold, "credentials")
client_secrets_file = os.path.join(secrets_and_credentials_fold, "client_secrets.json")
store = file.Storage(client_secrets_file )
creds = store.get()
#automatically renews google credentials
if creds.access_token_expired:
    creds.refresh(httplib2.Http())
#authorizing credentials
c = gspread.authorize(creds)
#gets spreadsheet
gs = c.open_by_key(sprsh)
#gets sheet by name
ws = gs.worksheet("Sheet1")

class Social_Media_Collector():


              def __init__(self, data ,row_number):

                             """
                             Managing the process of reading data from Social Media Spreadsheet,  setting from date option, passing
                             url, harvested, ui and date oprion to youtube collection and then passing the location to write_to_spreadsheet
                             function

                             data (list) - data from the of  google spreadsheet
                             row_number(int) - row_number

                             """
                             self.data = data
                             self.row_number = row_number
                             self.repeating = False

              def row_parser(self):

                             """
                             Parsing data list and directing to relevant harvester

                             """
                             self.ui = self.data[0]
                             self.description = self.data[1]
                             self.creator = self.data[2]
                             self.ready = self.data[3]
                             self.category = self.data[4]
                             self.location = self.data[5]
                             self.content_type = self.data[6]
                             self.link = self.data[7]
                             self.date_range = self.data[8]
                             self.sccope = self.data[9]
                             self.archived = self.data[10]
                             self.collected = self.data[11]
                             self.responsible = self.data[12]
                             self.storage_location = self.data[13]
                             self.notes = self.data[14]
                             self.flag = False
                             if "onwards" in self.date_range:
                                           self.repeating = True
                             
                             self.data[15] = self.repeating
                             self.data[16] = self.row_number
                             self.data[17] =project_folder
                             if            self.ready == "Y" and self.collected != "Y":
                                           my_harvester = Youtube_harvester(self.data)
                             #            if self.content_type == "InstagramAccount":
                             #                           flag, self.location = instagramm_account()
                             #            if self.content_type == "InstagramLive":
                             #                           flag, self.location = instagramm_live()
                             #            if self.content_type == "InstagramItem":
                             #                           flag, self.location = instagramm_item()
                             #            if self.content_type == "FacebookVideo":
                             #                           flag, self.location = facebook_video()
                             #            if self.content_type == "VimeoVideo":
                             #                           flag, self.location = vimeo_video()
                             #            if self.content_type == "TiktokVideo":
                             #                           flag, self.location = tiktok_video()
                             #            if self.content_type == "YoutubeVideo":
                             #                           flag, self.location = my_harvester.youtube_video()
                             #            if self.content_type == "YoutubChannel":
                             #                           flag, self.location = my_harvester.youtube_channel()
                                           print(self.content_type)
                                           if self.content_type == "YoutubeUser":
                                                          self.flag, self.location = my_harvester.youtube_user()
                                           if self.flag:
                                                          self.write_to_spreadsheet()

              def write_to_spreadsheet(self):

                             """
                             Writes to spreadsheet collect, responsible, storage location

                             """
                             ws.uodate_cell(self.row_number, 10, dt.now().stftime("%d.%m.%Y") )
                             ws.update_cell(self.row_number, 12, harvester)
                             ws.update_cell(self.row_number, 13, self.location)
                             if self.repeating:
                                           ws.update_cell(self.row_number, 11, "Y")

def main():

              """
              Initiates reading spreadsheet by rows

              """

              row_count  = ws.row_count
              for row_number, row in enumerate(ws.get_all_values()[1:], start = 2):
                             my_row = Social_Media_Collector(row, row_number)
                             my_row.row_parser()
                                           
if __name__ == "__main__":
              main()

