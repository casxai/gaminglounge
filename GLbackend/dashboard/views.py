from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from account.models import User
from post.models import Post, GameTitle
from .csv_processing import process_csv

from django.db.models import Count, Sum
from django.utils import timezone
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from account.forms import ProfileEditForm, ChangePasswordForm
from collections import defaultdict
import json

# Create your views here.


@login_required
def dashboard(request):
    admin = request.user
    # Total users count
    total_users_count = User.objects.count()

    # Total posts count
    total_posts_count = Post.objects.count()

    today = timezone.now().date()
    # Count the number of posts published today
    published_posts_today_count = Post.objects.filter(is_offensive=False, created_at__date=today).count()

    # Count the number of posts with foul words today
    foul_posts_today_count = Post.objects.filter(is_offensive=True, created_at__date=today).count()

    recent_published_posts = Post.objects.filter(is_offensive=False, created_at__date=today)[:3]
    recent_foul_posts = Post.objects.filter(is_offensive=True, created_at__date=today)[:3]

    # Count the number of games available in the community
    total_games_count = GameTitle.objects.count()

    # Count the number of likes for all posts
    all_posts = Post.objects.all()
    # Calculate total likes and comments for posts created on this day
    total_likes_count = all_posts.aggregate(Sum("likes_count"))["likes_count__sum"] or 0

    # GRAPH - LINE CHART
    # Create a dictionary to store counts for each day in November
    data_for_chart = defaultdict(lambda: {"published": 0, "foul": 0})

    # Set the start date as December 1st
    current_year = datetime.now().year
    start_date = datetime(current_year, 12, 1).date()

    # Loop through each day in November
    while start_date <= today and start_date.month == 12:
        # Count number of published posts
        allowed_posts_count = Post.objects.filter(is_offensive=False, created_at__date=start_date).count()

        # Count number of posts with detected foul words
        foul_posts_count = Post.objects.filter(is_offensive=True, created_at__date=start_date).count()

        # Store the counts for this day in the dictionary
        data_for_chart[start_date.strftime("%Y-%m-%d")] = {
            "published": allowed_posts_count,
            "foul": foul_posts_count,
        }

        # Move to the next day
        start_date += timedelta(days=1)

    # Sort the dictionary by keys (dates)
    sorted_data_for_chart = dict(sorted(data_for_chart.items()))
    json_data_for_chart = json.dumps(sorted_data_for_chart)


# --------
    # # Set the start date for each month
    # month = request.GET.get('month', '12')
    # current_year = datetime.now().year
    # start_date = datetime(current_year, int(month), 1).date()
    # end_date = start_date.replace(day=1, month=int(month) % 12 + 1) if int(month) != 12 else start_date.replace(year=current_year + 1, month=1)

    # while start_date < end_date:
    #     allowed_posts_count = Post.objects.filter(is_offensive=False, created_at__date=start_date).count()
    #     foul_posts_count = Post.objects.filter(is_offensive=True, created_at__date=start_date).count()

    #     data_for_chart[start_date.strftime("%Y-%m-%d")] = {
    #         "published": allowed_posts_count,
    #         "foul": foul_posts_count,
    #     }

    #     # Move to the next day
    #     start_date += timedelta(days=1)

    # # Sort the dictionary by keys (dates)
    # sorted_data_for_chart = dict(sorted(data_for_chart.items()))
    # json_data_for_chart = json.dumps(sorted_data_for_chart)

# ---------
    # POPULAR GAMES - PIE CHART
    top_games = (
        Post.objects.values("game_title__title")
        .annotate(num_posts=Count("id"))
        .order_by("-num_posts")[:5]
    )

    top_game_titles = [game["game_title__title"] for game in top_games]
    post_counts = [game["num_posts"] for game in top_games]

    # Serialize the data to JSON
    top_game_titles_json = json.dumps(top_game_titles)
    post_counts_json = json.dumps(post_counts)

    # ENGAGEMENT - LINE CHART
    # Create a dictionary to store the counts for each day in December
    data_for_engagement = defaultdict(int)
    engagement_start_date = datetime(current_year, 12, 1).date()
    # Set the start date as November 1st

    # Loop through each day in November
    while engagement_start_date <= today and engagement_start_date.month == 12:
        # Filter posts created on this day
        posts_on_day = Post.objects.filter(created_at__date=engagement_start_date)
        # Calculate total likes and comments for posts created on this day
        total_likes = (
            posts_on_day.aggregate(Sum("likes_count"))["likes_count__sum"] or 0
        )
        total_comments = (
            posts_on_day.aggregate(Sum("comments_count"))["comments_count__sum"] or 0
        )
        # Store the counts for this day in the dictionary
        data_for_engagement[engagement_start_date.strftime("%Y-%m-%d")] = {
            "likes": total_likes,
            "comments": total_comments,
        }

        # Move to the next day
        engagement_start_date += timedelta(days=1)
    # Sort the dictionary by keys (dates)
    sorted_data_for_engagement = dict(sorted(data_for_engagement.items()))
    json_data_for_engagement = json.dumps(sorted_data_for_engagement)

    context = {
        "admin_name": admin.name,
        "admin_email": admin.email,
        "admin_avatar": admin.avatar,
        "total_users_count": total_users_count,
        "total_posts_count": total_posts_count,
        "total_games_count": total_games_count,
        "total_likes_count": total_likes_count,
        "allowed_posts_today_count": published_posts_today_count,
        "foul_posts_today_count": foul_posts_today_count,
        "recent_published_posts": recent_published_posts,
        "recent_foul_posts": recent_foul_posts,
        "data_for_chart_json": json_data_for_chart,
        "top_game_titles_json": top_game_titles_json,
        "post_counts_json": post_counts_json,
        "json_data_for_engagement": json_data_for_engagement,
    }

    return render(request, "admin/index.html", context)

@login_required
def upload_csv(request):
    if request.method == 'POST' and 'csv_file' in request.FILES:  # Check if a file is uploaded
        csv_file = request.FILES['csv_file']  # Access the uploaded file

        # Pass the uploaded CSV file to the function for processing
        process_csv(csv_file)

        return JsonResponse({'message': 'File processed successfully'})
    return JsonResponse({'error': 'File upload failed'}, status=400)

# EDIT ADMIN
@login_required
def edit_profile(request):
    if request.method == "POST":
        profile_form = ProfileEditForm(
            request.POST, request.FILES, instance=request.user
        )

        if profile_form.is_valid():
            profile_form.save()
            return redirect("dashboard")
    else:
        profile_form = ProfileEditForm(instance=request.user)
        print(profile_form.errors)  # Check form errors in the console

    return render(request, "admin/edit_profile.html", {"profile_form": profile_form})


@login_required
def change_password(request):
    if request.method == "POST":
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            # Retrieve the new password from the form
            new_password = form.cleaned_data["new_password"]

            # Update the logged-in admin's password
            request.user.set_password(new_password)
            request.user.save()

            # Keep the user logged in after password change
            update_session_auth_hash(request, request.user)

            # Add a success message
            messages.success(request, "Your password has been successfully changed!")

            # Redirect to the 'editprofile/' page
            return redirect("edit_profile")
    else:
        form = ChangePasswordForm(user=request.user)  # Pass the user to the form

    return render(request, "admin/change_password.html", {"form": form})
