from image_downloader_module import *

#test for multiple media in one submission
name = 'your_user_name'

rid = RedditImageDownload(name)
rid.get_images(name_by = 'created_utc')