import django, os, requests, sys
from datetime import datetime
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

def get_group_feed(access_token):
    url = f"https://graph.facebook.com/v18.0/me?fields=groups%7Bname%2Cfeed%7Bid%2Cfull_picture%2Clink%2Cdescription%7D%7D&access_token={access_token}"

    response = requests.get(url)
    data = response.json()
    
    # Check for errors in the response
    if 'error' in data:
        raise Exception(f"Facebook API error: {data['error']['message']}")

    groups_data = data.get("groups", {}).get("data", [])
    return groups_data

access_token = "EAAMFfd1gTr8BO1JMtF4XZAg9RynWE8ZB1ZBgqgp2lGMfr37sYbEf89RDeHChinwZAo3QdRQIQ2aX5ze1Sx4CeZA2ZBOAUhfCW2d5uwXrhKNVSbGLKdsCPJsgrHrwFZBZCDES3mviGGPY7tZCaA6glReHB94qPZBDdUD1pYZAjVPUeOFl6YCr2yW5i8FdGs0"

# Get the group feed
group_feed = get_group_feed(access_token)

for group in group_feed:
    group_id = group["id"]
    game_title = group["name"]
    for post in group["feed"]["data"]:
        post_id = post.get("id", "N/A")
        if post_id != "N/A":
            body = post.get("description", "N/A")
            link = post.get("link", "N/A")
            full_picture = post.get("full_picture", "N/A")

            # Check the condition before creating a new Post instance
            if body != "N/A" and link != "N/A":
                user_id = "675a5aad3287452bba57b5aec4f60cc8"
                user_instance = User.objects.get(id=user_id)
                nav_bar = "Tournament"

                if game_title == "CALL OF DUTY":
                    game_name = 15
                elif game_title == "CALL OF DUTY_CONNECT":
                    game_name, nav_bar = 15, "Connect"
                elif game_title == "CALL OF DUTY_MARKETPLACE":
                    game_name, nav_bar = 15, "Marketplace"
                elif game_title == "FARLIGHT84":
                    game_name = 13                  
                # if game_title == "FARLIGHT84_CONNECT":
                #     game_name, nav_bar = 13, "Connect"
                elif game_title == "MOBILE LEGENDS":
                    game_name = 31
                elif game_title == "MOBILE LEGENDS_CONNECT":
                    game_name, nav_bar = 31, "Connect"
                elif game_title == "ML_MARKETPLACE":
                    game_name, nav_bar = 31, "Marketplace"
                elif game_title == "VALORANT":
                    game_name = 14
                elif game_title == "VALORANT_CONNECT":
                    game_name, nav_bar = 14, "Connect"
                elif game_title == "VALORANT_MARKETPLACE":
                    game_name, nav_bar = 14, "Connect"
                elif game_title == "BETA-TESTING":
                    game_name, nav_bar = 34, "Beta Testing"

                existing_post = Post.objects.filter(outside_id=post_id).exists()

                if not existing_post:
                    # Create a new Post instance
                    new_post = Post.objects.create(
                        body=body,
                        created_at=formatted_datetime,
                        created_by_id=user_instance.id,
                        is_private=False,
                        game_title_id=game_name,
                        post_url=link,
                        outside_id=post_id,
                        menu=nav_bar,
                    )

                    User.objects.filter(id=user_id).update(posts_count=F("posts_count") + 1)

                    new_attachment = PostAttachment.objects.create(
                        image_url=full_picture, created_by=user_instance
                    )
                    new_post.attachments.add(new_attachment)



