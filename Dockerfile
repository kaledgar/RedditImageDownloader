FROM python:3.10
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
VOLUME /app/downloads

# download images from yout_user_name
CMD ["python3", "-m", "reddit_image_downloader", "-u", "your_user_name" ]
