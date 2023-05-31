import os
from pyrogram import Client
from pyrogram.errors import FloodWait, AccessTokenExpired
import random
import pymongo
import requests
from bs4 import BeautifulSoup

directory_path = "./Infinityprn/Videos"
# Replace YOUR_API_ID and YOUR_API_HASH with your own values
api_id = 2448614
api_hash = 'c1c1a85c23643876d4ae5c76b20e821f'


tokens = ["6148509956:AAF05cgppFbAM5oZVYjpjqfRtJWTFoQ786Q","5987433096:AAGxrel-GjJb-VryGj3K4GBPn4ZbPL4-c9c","5928285583:AAEK8qamRXuajFrZP3pFOMti-r4VOQ4uhaM"]
chatid=int(-1819740146)


MONGO_URL = "mongodb+srv://personaluse:ImCrAzYbOy@personaluse.ounsjuz.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(MONGO_URL)
db = client["X-HAMSTER-20"]
pagedb = db["PAGES"]
videosdb = db["VIDEOS20DESI"]
url = ['https://xhamster20.desi/videos/behind-the-scenes-with-james-deen-morgan-lee-anal-9244410']
filtered_links = []
videoslist = []

for l in pagedb.find({}):
    link = l['url']
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all(class_="video-thumb__image-container role-pop thumb-image-container")
    for hre in links:
        s = hre.get('href')
        if s and s.startswith('https://xhamster20.desi/videos/'):
            print(s)
            url.append(s)
            pagedb.insert_one({'url': s})
            t = requests.get(s)
            vlink = BeautifulSoup(t.content, "html.parser")
            vli = soup.find_all("a")
            title = soup.title.string
            image_url = soup.find('meta', {'property': 'og:image'})['content']
            for i in vli:
                t = i.get('href')
                if t and t.startswith("https://19-18.b.cdn13.com/"):
                    auers = videosdb.find_one({"url": t})
                    if auers is not None:
                        da = "as"
                    else:
                        print(t)
                        videosdb.insert_one({'url': t})
                        video = requests.get(t)
                        img = requests.get(image_url)
                        filename = s.split("/")[-1]
                        with open(f"{directory_path}/{filename}.mp4.jpg", "wb") as i:
                            i.write(img.content)
                        with open(f"{directory_path}/{filename}.mp4", "wb") as f:
                            f.write(video.content)
                        name = random.choice(tokens)
                        try:
                            with Client(name, api_id, api_hash, bot_token=name) as app:
                                try:
                                    for filename in os.listdir(directory_path):
                                        if filename.endswith('.mp4'):
                                            with open(f"{directory_path}/{filename}", 'rb') as f, open(f"{directory_path}/{filename}.jpg", "rb") as i:
                                                try:
                                                    app.send_video(chatid,f,thumb=i)
                                                    os.remove(f"{directory_path}/{filename}")
                                                    os.remove(f"{directory_path}/{filename}.jpg")
                                                except AccessTokenExpired as ATE:
                                                    tokens.remove(name)
                                                    videosdb.delete_one({'url': s})
                                                    os.remove(f"{directory_path}/{filename}")
                                                    os.remove(f"{directory_path}/{filename}.jpg")
                                                except FloodWait as e:
                                                    print(f"Sleeping For {e.x} secs!")
                                                    time.sleep(e.x)
                                                    app.send_video(chatid, f,thumb=i)
                                                    os.remove(f"{directory_path}/{filename}")
                                                    os.remove(f"{directory_path}/{filename}.jpg")
                                                except Exception as error:
                                                    print(f"Error During Uploading: {error}")
                                                    videosdb.delete_one({'url': s})
                                                    os.remove(f"{directory_path}/{filename}")
                                                    os.remove(f"{directory_path}/{filename}.jpg")
                                except Exception as tb:
                                    print(f"Error Wile opening file {tb}")
                        except FloodWait as e:
                            print(f"Sleeping For {e.x} secs!")
                            time.sleep(e.x)
                            
