from image_downloader_module import *

#test for multiple media in one submission
name = 'your_user_name'

rid = RedditImageDownload(name)
df = rid._get_posts()
df1 = rid.classify_urls(df)

print(df1.to_string())