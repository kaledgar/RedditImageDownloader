from image_downloader_module import *

#test for multiple media in one submission
#name1 = 'vegetaaaa88'
name = 'YuzuPyon'

rid = RedditImageDownload(name)
df = rid._get_posts()
df1 = rid.classify_urls(df)

print(df1.to_string())

rid.get_images(name_by='id')