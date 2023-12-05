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

csv_file_path = r"E:\Codes\Capstone\gaming-lounge\GLbackend\post\data.csv"

# Read data from the CSV file and insert into the Django Post model
with open(csv_file_path, "r", encoding="utf-8") as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Skip the header row if it exists

    for row in csv_reader:
        # Assuming your CSV file has three columns: column1, column2, column3
        (
            dataname,
            dataselftext,
            datatitle,
            datasubreddit,
            dataurl,
            datathumbnail,
            nav_bar,
        ) = row
        if datasubreddit == "Eldenring" or datasubreddit == "ELDEN RING":
            datasubreddit = 9
        elif datasubreddit == "Genshin_impact" or datasubreddit == "GENSHIN IMPACT":
            datasubreddit = 10
        elif datasubreddit == "l4d2" or datasubreddit == "LEFT 4 DEAD":
            datasubreddit = 11
        elif datasubreddit == "Minecraft" or datasubreddit == "MINECRAFT":
            datasubreddit = 12
        elif datasubreddit == "Farlight84" or datasubreddit == "FARLIGHT":
            datasubreddit = 13
        elif datasubreddit == "VALORANT" or datasubreddit == "VALORANT":
            datasubreddit = 14
        elif datasubreddit == "CallOfDuty" or datasubreddit == "CALL OF DUTY":
            datasubreddit = 15
        elif datasubreddit == "counterstrike" or datasubreddit == "COUNTER STRIKE":
            datasubreddit = 16
        elif datasubreddit == "PUBG" or datasubreddit == "PUBG":
            datasubreddit = 17
        elif (
            datasubreddit == "footballmanagergames"
            or datasubreddit == "FOOTBALL MANAGER"
        ):
            datasubreddit = 18
        elif datasubreddit == "RocketLeague" or datasubreddit == "ROCKET LEAGUE":
            datasubreddit = 19
        elif datasubreddit == "leagueoflegends" or datasubreddit == "LEAGUE OF LEGENDS":
            datasubreddit = 20
        elif datasubreddit == "DotA2" or datasubreddit == "DOTA 2":
            datasubreddit = 21
        elif datasubreddit == "Sims4" or datasubreddit == "SIMS":
            datasubreddit = 22
        elif datasubreddit == "roblox" or datasubreddit == "ROBLOX":
            datasubreddit = 23
        elif datasubreddit == "Tekken" or datasubreddit == "TEKKEN":
            datasubreddit = 24
        elif datasubreddit == "FinalFantasy" or datasubreddit == "FINAL FANTASY":
            datasubreddit = 25
        elif datasubreddit == "smashbros" or datasubreddit == "SUPER SMASH BRO":
            datasubreddit = 26
        elif datasubreddit == "PhasmophobiaGame" or datasubreddit == "PHASMOPHOBIA":
            datasubreddit = 27
        elif datasubreddit == "diablo4" or datasubreddit == "DIABLO 4":
            datasubreddit = 28
        elif datasubreddit == "GrandTheftAutoV" or datasubreddit == "GTA 5":
            datasubreddit = 29
        elif datasubreddit == "MonsterHunter" or datasubreddit == "MONSTER HUNTER":
            datasubreddit = 30
        elif datasubreddit == "MobileLegendsGame" or datasubreddit == "MOBILE LEGENDS":
            datasubreddit = 31
        elif datasubreddit == "NBA2k" or datasubreddit == "NBA":
            datasubreddit = 32
        elif datasubreddit == "ForzaHorizon" or datasubreddit == "FORZA HORIZON 5":
            datasubreddit = 33
        else:
            datasubreddit = 34

        body_text = f"{datatitle}\n{dataselftext}"

        # Assuming you have the user's ID or another way to identify the user
        user_id = "3e9fe50b5c31439f9fb68208a5c3dba9"
        user_instance = User.objects.get(id=user_id)

        # Create a new Post instance
        new_post = Post.objects.create(
            body=body_text,
            created_at=formatted_datetime,
            created_by_id=user_instance.id,
            is_private=False,
            game_title_id=datasubreddit,
            post_url=dataurl,
            outside_id=dataname,
            menu=nav_bar,
        )

        # Increment post_count in User model by 1 after creating a new post
        User.objects.filter(id=user_id).update(posts_count=F("posts_count") + 1)

        new_attachment = PostAttachment.objects.create(
            image_url=datathumbnail, created_by=user_instance
        )

        # Link this attachment to the specific Post instance
        new_post.attachments.add(new_attachment)
