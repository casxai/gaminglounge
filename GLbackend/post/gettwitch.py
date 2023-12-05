import requests
import sqlite3
from datetime import datetime
import os
import django
import sys
from django.db.models import F
import sys
import io

# Change the standard output encoding to 'utf-8'
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), ".."))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GLbackend.settings")
django.setup()

from post.models import Post, PostAttachment
from account.models import User

# Get the current date and time
current_datetime = datetime.now()

# Format the datetime as a string (you can adjust the format as needed)
formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")


# Set the necessary parameters
CLIENT_ID = "2son5pbomhy29mng0zhzduqriouerl"
CLIENT_SECRET = "j0djntmdw9mt269ar6ao1b3qfu96h1"
USER_LOGINS = [
    "lunacuddles",
    "button",
    "kioshizumi",
    "kyedae",
    "kodopro",
    "tmi98",
    "xbultx",
    "loltyler1",
    "Dendi",
    "plinkztv",
    "christoyfu27",
]  # Replace with the actual streamer's username

# Provide the absolute path to your db.sqlite3 file
db_path = r"E:\Codes\Capstone\gaming-lounge\GLbackend\db.sqlite3"

# Connect to the existing SQLite database
conn = sqlite3.connect(db_path)
# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Make a request to get the OAuth token
token_response = requests.post(
    f"https://id.twitch.tv/oauth2/token"
    f"?client_id={CLIENT_ID}"
    f"&client_secret={CLIENT_SECRET}"
    "&grant_type=client_credentials"
)

if token_response.status_code == 200:
    access_token = token_response.json()["access_token"]
    headers = {"Client-ID": CLIENT_ID, "Authorization": f"Bearer {access_token}"}

    for USER_LOGIN in USER_LOGINS:
        # Get the user ID for the streamer
        user_response = requests.get(
            f"https://api.twitch.tv/helix/users?login={USER_LOGIN}", headers=headers
        )

        if user_response.status_code == 200:
            user_data = user_response.json()
            if user_data["data"]:
                user_id = user_data["data"][0]["id"]
                params = {
                    "user_id": user_id,
                    "first": 5,  # Retrieve the first 5 videos, adjust as needed
                    "sort": "time",  # Sort the videos by time
                }

                # Make the GET request to the Twitch API with the OAuth token
                response = requests.get(
                    "https://api.twitch.tv/helix/videos", headers=headers, params=params
                )

                # Handle the API response
                if response.status_code == 200:
                    data = response.json()
                    if data["data"]:
                        for video in data["data"]:
                            video_title = video["title"]
                            video_url = f"https://www.twitch.tv/videos/{video['id']}"
                            post_id = video["id"]
                            thumbnail_url = video["thumbnail_url"]
                            view_count = video["view_count"]

                            if USER_LOGIN == "valorant":
                                game_title = 9
                            elif USER_LOGIN == "lunacuddles":
                                game_title = 10
                            elif USER_LOGINS == "minecraft":
                                game_title = 11
                            elif USER_LOGIN == "button":
                                game_title = 12
                            elif USER_LOGIN == "kioshizumi":
                                game_title = 13
                            elif USER_LOGIN == "kyedae":
                                game_title = 14
                            elif USER_LOGIN == "kodopro":
                                game_title = 15
                            elif USER_LOGIN == "tmi98":
                                game_title = 16
                            elif USER_LOGIN == "minecraft":
                                game_title = 17
                            elif USER_LOGIN == "minecraft":
                                game_title = 18
                            elif USER_LOGIN == "xbultx":
                                game_title = 19
                            elif USER_LOGIN == "loltyler1":
                                game_title = 20
                            elif USER_LOGIN == "Dendi":
                                game_title = 21
                            elif USER_LOGIN == "minecraft":
                                game_title = 22
                            elif USER_LOGIN == "plinkztv":
                                game_title = 23
                            elif USER_LOGIN == "minecraft":
                                game_title = 24
                            elif USER_LOGIN == "minecraft":
                                game_title = 25
                            elif USER_LOGIN == "minecraft":
                                game_title = 26
                            elif USER_LOGIN == "minecraft":
                                game_title = 27
                            elif USER_LOGIN == "minecraft":
                                game_title = 28
                            elif USER_LOGIN == "minecraft":
                                game_title = 29
                            elif USER_LOGIN == "minecraft":
                                game_title = 30
                            elif USER_LOGIN == "christoyfu27":
                                game_title = 31
                            elif USER_LOGIN == "minecraft":
                                game_title = 32
                            elif USER_LOGIN == "minecraft":
                                game_title = 33
                            else:
                                game_title = 34

                            print(
                                f"Inserted video data for {USER_LOGIN}: {video_title}"
                            )
                            user_id = "1cfff9f31d814cb09028c3376871a4bb"
                            user_instance = User.objects.get(id=user_id)

                            # Create a new Post instance
                            new_post = Post.objects.create(
                                body=video_title,
                                created_at=formatted_datetime,
                                created_by_id=user_instance.id,
                                is_private=False,
                                game_title_id=game_title,
                                post_url=video_url,
                                outside_id=post_id,
                            )

                            User.objects.filter(id=user_id).update(
                                posts_count=F("posts_count") + 1
                            )

                            new_attachment = PostAttachment.objects.create(
                                image_url=thumbnail_url, created_by=user_instance
                            )
                            new_post.attachments.add(new_attachment)

                    else:
                        print(f"No videos found for the user {USER_LOGIN}.")
                else:
                    print(f"Error: {response.status_code} - {response.text}")
            else:
                print(f"No user found with the username {USER_LOGIN}.")
        else:
            print(f"Error: {user_response.status_code} - {user_response.text}")
