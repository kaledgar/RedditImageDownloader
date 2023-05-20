from image_downloader_module import *

#test for multiple media in one submission
name1 = 'your_user_name'

rid = RedditImageDownload(name1)
x = rid.get_images(name_by = 'created_utc')
