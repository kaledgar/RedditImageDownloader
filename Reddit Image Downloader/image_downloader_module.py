import pandas as pd
import json
import praw
import requests
import os
import logging
from datetime import datetime
## add error handling!!!!!!!
from prawcore.exceptions import Forbidden
from constants import *

logger = logging.getLogger(__name__)

class RedditImageDownload:
    def __init__(self, user_name, credentials_filepath=DEFAULT_CREDENTIALS_FILEPATH):
        self.user_name = user_name
        self.reddit = self._get_reddit_from_filepath(credentials_filepath)
        self.user = self.reddit.redditor(self.user_name)

    def _get_reddit_from_filepath(self, credentials_filepath):
        with open(credentials_filepath, "r") as file:
            credentials = json.load(file)
        return praw.Reddit(
            client_id=credentials["client_id"],
            client_secret=credentials["client_secret"],
            password=credentials["password"],
            user_agent=credentials["user_agent"],
            username=credentials["username"],
        )

    def _make_directory(self):
        path = f'./{self.user_name}'
        if not os.path.exists(path):
            os.mkdir(path)
            print(f"Folder {path} created!")
        else:
            print(f"Folder {path} already exists")

    def _get_posts(self, posts_count=POST_COUNT):
        user_submissions = [
            (subm.id, subm.url, subm.created_utc)
            for subm in self.user.submissions.new(limit=None)
        ]
        df = pd.DataFrame(user_submissions, columns=["id", "url", "created_utc"])
        logger.debug(f'{self.user_name} posts: {df}')
        return df

    def _get_posts_from_profile(self, posts_count=POST_COUNT):
        profile = self.user.subreddit.display_name
        subreddit = self.reddit.subreddit(profile)
        post_info = [
            (
                subm.id,
                str(subm.author),
                str(subm.url),
                str(subm.title),
                int(subm.created_utc),
                subm.subreddit,
            )
            for subm in subreddit.top(limit=posts_count)
        ]
        df = pd.DataFrame(
            post_info,
            columns=[
                "id",
                "author",
                "text",
                "url",
                "title",
                "score",
                "created_utc",
                "subreddit",
            ],
        )
        return df

    def download_from_url(self, url, name, format):
        rqst = requests.get(url)

        with open(f'{name}.{format}', "wb") as file:
            file.write(rqst.content)

    def classify_urls(self, df):
        df['type'] = df['url'].apply(
            lambda x: 'image'
            if 'i.redd.it' in x
            else 'gallery' if 'reddit.com/gallery' in x
            else 'unknown')
        return df

    def get_images(self, name_by = 'id'):
        #check if directory exists:
        if os.path.isdir(f'{self.user_name}') == False:
            self._make_directory()
        else:
            logger.info(f'Directory /{self.user_name} already exists')
        self._make_directory()
        df = self._get_posts()

        #loop through urls dataframe and download images to dir
        for i, url in enumerate(df['url']):
            if name_by == 'id':
                name_i = df['id'][i]
            elif name_by == 'created_utc':
                #unix time
                #name_i = df['created_utc'][i]
                #YYYY-MM-DD--hh-mm-ss
                name_i = datetime.utcfromtimestamp(df['created_utc'][i]).strftime('%Y-%m-%d--%H-%M-%S')

            filepath = f'{self.user_name}/{name_i}'
            self.download_from_url(url, filepath, 'jpg')

        return df

    def test_gallery(self, gallery_id):
        post = self.reddit.submission(id=gallery_id)
        gallery = []
        for i in post.media_metadata.items():
            url = i[1]['p'][0]['u']
            url = url.split("?")[0].replace("preview", "i")
            gallery.append(url)

        return gallery

'''rid = RedditImageDownload('vegetaaaa88')
r = rid.test_gallery(gallery_id = '13bmz4e')

print(r)'''