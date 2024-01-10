import requests
from datetime import datetime
import os
import django
import sys
import io
import pytz

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
    "PengguWonu",
    "kyedae",
    "kodopro",
    "tmi98",
    # "xbultx",
    "loltyler1",
    "Dendi",
    "WikyamYT",
    "christoyfu27",
]  # Replace with the actual streamer's username


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
                    "first": 1,  # Retrieve the first 5 videos, adjust as needed
                    "sort": "time",  # Sort the videos by time in descending order
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
                            # Extract the posting date and time
                            posting_datetime = datetime.strptime(
                                video["created_at"], "%Y-%m-%dT%H:%M:%SZ"
                            )

                            philippine_timezone = pytz.timezone('Asia/Manila')
                            posting_datetime_convert = posting_datetime.replace(tzinfo=pytz.utc).astimezone(philippine_timezone)

                            # Convert posting_datetime_ph to a naive datetime (without timezone)
                            posting_datetime_ph = posting_datetime_convert.replace(tzinfo=None)

                            # Calculate the time difference
                            time_difference = current_datetime - posting_datetime_ph
                            print(f"Time Difference: {time_difference}")
                            # Check if the video was posted within the last 24 hours
                            if time_difference.total_seconds() <= 24 * 3600:
                                formatted_posting_datetime = posting_datetime_ph.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                )

                                video_title = video["title"]
                                video_url = f"https://www.twitch.tv/videos/{video['id']}"
                                post_id = video["id"]
                                # thumbnail_url = video["thumbnail_url"]
                                view_count = video["view_count"]

                                if USER_LOGIN == "lunacuddles":
                                    game_title = 10
                                elif USER_LOGIN == "button":
                                    game_title = 12
                                elif USER_LOGIN == "PengguWonu":
                                    game_title = 13
                                elif USER_LOGIN == "kyedae":
                                    game_title = 14
                                elif USER_LOGIN == "kodopro":
                                    game_title = 15
                                elif USER_LOGIN == "tmi98":
                                    game_title = 16
                                # elif USER_LOGIN == "xbultx":
                                #     game_title = 19
                                elif USER_LOGIN == "loltyler1":
                                    game_title = 20
                                elif USER_LOGIN == "Dendi":
                                    game_title = 21
                                elif USER_LOGIN == "WikyamYT":
                                    game_title = 23
                                elif USER_LOGIN == "christoyfu27":
                                    game_title = 31
                                else:
                                    game_title = 34

                                print(
                                    f"Inserted video data for {USER_LOGIN}: {video_title}"
                                )
                                user_id = "1cfff9f31d814cb09028c3376871a4bb"
                                user_instance = User.objects.get(id=user_id)
                                existing_post = Post.objects.filter(outside_id=post_id).exists()

                                if not existing_post:
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

                    else:
                        print(f"No videos found for the user {USER_LOGIN}.")
                else:
                    print(f"Error: {response.status_code} - {response.text}")
            else:
                print(f"No user found with the username {USER_LOGIN}.")
        else:
            print(f"Error: {user_response.status_code} - {user_response.text}")
