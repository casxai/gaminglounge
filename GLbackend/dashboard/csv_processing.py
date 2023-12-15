# csv_processing.py

import csv
from io import TextIOWrapper
from datetime import datetime
from post.models import Post, PostAttachment
from account.models import User  # Assuming your User model is in account.models


def process_csv(csv_file):
    # Get the current date and time
    current_datetime = datetime.now()

# Format the datetime as a string (you can adjust the format as needed)
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    user_id = "675a5aad3287452bba57b5aec4f60cc8"  # Replace with your actual user ID
    user_instance = User.objects.get(id=user_id)  # Get the user instance

    # Get the file handle or path from the InMemoryUploadedFile object
    file_handle = csv_file.file if hasattr(csv_file, 'file') else csv_file

    with TextIOWrapper(file_handle, encoding='utf-8') as file_wrapper:
        csv_reader = csv.reader(file_wrapper)
        next(csv_reader)  # Skip the header row if it exists

        for row in csv_reader:
            (
                body,
                game_title_id,
                post_url,
                outside_id,
                image_url,
                menu,
            ) = row

            # Process data and create Post and PostAttachment instances
            
            # body_text = f"{datatitle}\n{dataselftext}"

            new_post = Post.objects.create(
                body=body,
                created_at=formatted_datetime,
                created_by_id=user_instance.id,
                is_private=False,
                game_title_id=game_title_id,
                post_url=post_url,
                outside_id=outside_id,
                menu=menu,
            )


            new_attachment = PostAttachment.objects.create(
                image_url=image_url,
                created_by=user_instance
            )

            new_post.attachments.add(new_attachment)
