FROM python:3.10
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
VOLUME .

# download images from "user1" and "user2" 
CMD ["python3", "-m", "reddit_image_downloader", "-u", "user1", "user2", "user3"]
