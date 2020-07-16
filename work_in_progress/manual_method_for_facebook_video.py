import re

""" 
You need a facebook account url, e.g. https://www.facebook.com/pg/jacindaardern. 

Manually resolve the videos page in a browser,  https://www.facebook.com/pg/jacindaardern/videos

and scroll for as much as is needed to build the thumbnails (and therefore links) over the range you want. 

Save this page from the browser as html

You don't need the assets, only page - so use save as .html, but if you want to capture them as the original thumbnails, use save as .mhtml)

For this script, the html file is called "my_facebook_video_page.html"

You will need to check the first few links - they won't be to videos. 

The pattern for video urls you want is:

	https://www.facebook.com/jacindaardern/videos/{facebook_video_id}/

"""

my_html = "my_facebook_video_page.html"

my_url = "https://www.facebook.com/pg/jacindaardern/videos"


with open (my_html, encoding="utf8") as data:
	s = data.read()



for h in  re.findall(r'href=[\'"]?([^\'" >]+)', s):
	if "video" in h and h.startswith("https") and h != f"{my_url}/#" and h !=f"{my_url}/":
		print (h)


