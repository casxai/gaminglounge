import json
import requests
import sqlite3
import csv
from datetime import datetime
import os
import django
import sys
from django.db.models import F

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), ".."))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GLbackend.settings")
django.setup()

from post.models import Post, PostAttachment
from account.models import User

# Get the current date and time
current_datetime = datetime.now()

# Format the datetime as a string (you can adjust the format as needed)
formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

def extend_access_token(app_id, app_secret, short_lived_token):
    # Construct the URL for token exchange
    url = f"https://graph.facebook.com/v18.0/oauth/access_token?grant_type=fb_exchange_token&client_id={app_id}&client_secret={app_secret}&fb_exchange_token={short_lived_token}"
    
    try:
        # Make a request to the Facebook Graph API
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()  # Parse the JSON response

        # Check for errors in the response
        if 'error' in data:
            raise Exception(f"Facebook API error: {data['error']['message']}")

        long_lived_token = data.get("access_token")
        return long_lived_token

    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Something went wrong:", err)

    return None

def get_group_feed(access_token):
    url = f"https://graph.facebook.com/v18.0/me?fields=groups%7Bid%2Cname%2Cfeed%7Bid%2Cfull_picture%2Clink%2Cdescription%7D%7D&access_token={access_token}"
    response = requests.get(url)
    data = response.json()
    
    # Check for errors in the response
    if 'error' in data:
        raise Exception(f"Facebook API error: {data['error']['message']}")

    return data.get('groups', {}).get('data', [])

app_id = '850463073259199'
app_secret = '3700040e1e94d3dc3f5dc14b61c6718b'
short_lived_token = 'EAAMFfd1gTr8BO37DDruv0DdxpNrJF5cLpcHrYZB2kUbdpOmSx5jZBxLS9FGyB8TtfakkBVrf0lK7j9YaZAV2CMp4HWcZAtAkiYhoAWNgpIxZCDuysmIYCeUTvHSQNTxcJbdsRSZBELSizDZCujgEgYZANTDV4vZBFUsH1tBgJaaK9L3OMjU0cL9lLEpmkWDWLn6ZARBNE9VCRRGmXnNnHhbdqoCDZCdxZBS9EOStYJF8nthdOEwg9cZCHnJRuK3eoodIJpwZDZD'

# Use the function to get a long-lived token
long_lived_token = extend_access_token(app_id, app_secret, short_lived_token)

# Replace the access token with the long-lived token
access_token = long_lived_token
# Use the user access token you obtained

# Get the group feed
group_feed = get_group_feed(access_token)

# Loop through the data and insert into the existing SQLite database
for group in group_feed:
    group_id = group.get('id')
    game_name = group.get('name')
    for post in group['feed']['data']:
        post_id = post.get('id', 'N/A')
        if post_id != 'N/A':
            body = post.get('description', 'No message available')
            link = post.get('link', 'No link available')
            full_picture = post.get('full_picture', 'No picture available')          
            user_id = '675a5aad3287452bba57b5aec4f60cc8'
            user_instance = User.objects.get(id=user_id)

            if game_name == "FARLIGHT84_CONNECT":
                game_title, nav_bar = 13, "Connect"
            elif game_name == "GENSHIN IMPACT":
                game_title = 10
            elif game_name == "FARLIGHT84":
                game_title = 13
            elif game_name == "VALORANT":
                game_title = 14
            elif game_name == "CALL OF DUTY":
                game_title = 15
            elif game_name == "CALL OF DUTY_CONNECT":
                game_title, nav_bar = 15, "Connect"
            elif game_name == "COUNTER STRIKE":
                game_title = 17
            elif game_name == "PUBG":
                game_title = 18
            elif game_name == "LEAGUE OF LEGENDS":
                game_title = 20
            elif game_name == "DOTA 2":
                game_title = 21
            elif game_name == "VALORANT_CONNECT":
                game_title, nav_bar = 14, "Connect"
            elif game_name == "MOBILE LEGENDS_CONNECT":
                game_title, nav_bar = 31, "Connect"
            elif game_name == "CALL OF DUTY_MARKETPLACE":
                game_title, nav_bar = 15, "Marketplace"
            elif game_name == "BETA-TESTING":
                game_title, nav_bar = 34, "Beta Testing"
            elif game_name == "MOBILE LEGENDS":
                game_title = 31
            elif game_name == "NBA 2K":
                game_title = 32
            else:
                game_title = 34

            if post_id != 'N/A' and not Post.objects.filter(outside_id=post_id).exists():
            # Create a new Post instance
                new_post = Post.objects.create(
                    body=body,
                    created_at=formatted_datetime,
                    created_by_id=user_instance.id,
                    is_private=False,
                    game_title_id=game_title,
                    post_url=link,
                    outside_id=post_id,
                    menu=nav_bar,
                )

                print('new-post',new_post)

                new_attachment = PostAttachment.objects.create(
                    image_url=full_picture, 
                    created_by=user_instance
                )
                new_post.attachments.add(new_attachment)

print('new-post',new_post)




# import requests
# from datetime import datetime
# import os, django, sys
# from django.db.models import F

# sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), ".."))
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GLbackend.settings")
# django.setup()

# from post.models import Post, PostAttachment
# from account.models import User

# # Get the current date and time
# current_datetime = datetime.now()

# # Format the datetime as a string (you can adjust the format as needed)
# formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")


# def get_group_feed(access_token):
#     url = f"https://graph.facebook.com/v18.0/me?fields=groups%7Bfeed%7Bid%2Cfull_picture%2Clink%2Cdescription%7D%2Cid%2Cname%7D&access_token={access_token}"
#     response = requests.get(url)
#     data = response.json()
#     return data["groups"]["data"]



# # Use the user access token you obtained
# access_token = "EAAMFfd1gTr8BO6ZBKjNAnA2rtsIO4HvLVFGXOJ03xZAMt6hCblw4FySSI7yvVpK4Rh7gGdKWUPVZAgH8YWF2Es71SenRoAmz0fd73VpJFrRNlyClwkalpTAbZBo93e6VGZAZBpQ2XHGbPzvN9sVX84WPEqryYZBtUZCGbPFTuyboUcQDpvYWMvtFMGn7i8hUamL3L8PN7LNe939N9JGV1QuaiFt6GUUXOtRXjTKq1to9MLqQe8Usn2xZARrrzt4N4YwZDZD"

# # Get the group feed
# group_feed = get_group_feed(access_token)

# # Loop through the data and insert into the existing SQLite database
# for group in group_feed:
#     group_id = group["id"]
#     game_title = group["name"]
#     for post in group["feed"]["data"]:
#         post_id = post.get("id", "N/A")
#         if post_id != "N/A":
#             body = post.get("description", "N/A")
#             link = post.get("link", "N/A")
#             full_picture = post.get("full_picture", "N/A")

#             # Check the condition before creating a new Post instance
#             if body != "N/A" and link != "N/A":
#                 user_id = "675a5aad3287452bba57b5aec4f60cc8"
#                 user_instance = User.objects.get(id=user_id)
#                 nav_bar = "Tournament"

#                 if game_title == "FARLIGHT84_CONNECT":
#                     game_name, nav_bar = 13, "Connect"
#                 elif game_title == "GENSHIN IMPACT":
#                     game_name = 10
#                 elif game_title == "minecraft":
#                     game_name = 11
#                 elif game_title == "MINECRAFT":
#                     game_name = 12
#                 elif game_title == "FARLIGHT84":
#                     game_name = 13
#                 elif game_title == "VALORANT":
#                     game_name = 14
#                 elif game_title == "CALL OF DUTY":
#                     game_name = 15
#                 elif game_title == "CALL OF DUTY_CONNECT":
#                     game_name, nav_bar = 15, "Connect"
#                 elif game_title == "COUNTER STRIKE":
#                     game_name = 17
#                 elif game_title == "PUBG":
#                     game_name = 18
#                 elif game_title == "ROCKET LEAGUE":
#                     game_name = 19
#                 elif game_title == "LEAGUE OF LEGENDS":
#                     game_name = 20
#                 elif game_title == "DOTA 2":
#                     game_name = 21
#                 elif game_title == "minecraft":
#                     game_name = 22
#                 elif game_title == "VALORANT_CONNECT":
#                     game_name, nav_bar = 14, "Connect"
#                 elif game_title == "TEKKEN":
#                     game_name = 24
#                 elif game_title == "MOBILE LEGENDS_CONNECT":
#                     game_name, nav_bar = 31, "Connect"
#                 elif game_title == "CALL OF DUTY_MARKETPLACE":
#                     game_name, nav_bar = 15, "Marketplace"
#                 elif game_title == "minecraft":
#                     game_name = 27
#                 elif game_title == "DIABLO 4":
#                     game_name = 28
#                 elif game_title == "minecraft":
#                     game_name = 29
#                 elif game_title == "BETA-TESTING":
#                     game_name, nav_bar = 34, "Beta Testing"
#                 elif game_title == "MOBILE LEGENDS":
#                     game_name = 31
#                 elif game_title == "NBA 2K":
#                     game_name = 32
#                 elif game_title == "FORZA HORIZON 5":
#                     game_name = 33
#                 else:
#                     game_name = 34

#                 # Create a new Post instance
#                 new_post = Post.objects.create(
#                     body=body,
#                     created_at=formatted_datetime,
#                     created_by_id=user_instance.id,
#                     is_private=False,
#                     game_title_id=game_name,
#                     post_url=link,
#                     outside_id=post_id,
#                     menu=nav_bar,
#                 )

#                 User.objects.filter(id=user_id).update(posts_count=F("posts_count") + 1)

#                 new_attachment = PostAttachment.objects.create(
#                     image_url=full_picture, created_by=user_instance
#                 )
#                 new_post.attachments.add(new_attachment)

