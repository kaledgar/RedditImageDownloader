import requests

from image_downloader_module import RedditImageDownload

url = 'https://mxj.myanimelist.net/img/projects/readthismanga/2023/index/img-chara.png'

req = requests.get(url)

name = 'aaa'
format = 'png'
with open(f'{name}.{format}', "wb") as f:
    f.write(req.content)