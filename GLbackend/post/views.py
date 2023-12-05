from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Count
from django.utils import timezone
from .best_profanity import has_profanity  # profcheck
from .models import Post, GameTitle
from .forms import PostForm, AddPostForm, EditPostForm
from rest_framework.response import Response  # profcheck


import uuid


def admin_posts(request):
    admin = request.user

    posts = Post.objects.all()
    posts_allowed = Post.objects.filter(is_offensive=False)
    posts_blocked = Post.objects.filter(is_offensive=True)

    total_posts_count = Post.objects.count()
    discussion_posts = Post.objects.filter(menu="Discussions").count()
    tournament_posts = Post.objects.filter(menu="Tournament").count()
    connect_posts = Post.objects.filter(menu="Connect").count()
    marketplace_posts = Post.objects.filter(menu="Marketplace").count()
    beta_posts = Post.objects.filter(menu="Beta Testing").count()

    context = {
        "admin_name": admin.name,
        "admin_email": admin.email,
        "admin_avatar": admin.avatar,
        "total_posts_count": total_posts_count,
        "discussion_posts": discussion_posts,
        "tournament_posts": tournament_posts,
        "connect_posts": connect_posts,
        "marketplace_posts": marketplace_posts,
        "beta_posts": beta_posts,
        "posts": posts,
        "posts_allowed": posts_allowed,
    }
    return render(request, "admin/posts.html", context)


def add_post(request):
    if request.method == "POST":
        form = AddPostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.created_by = request.user
            new_post.save()
            return redirect("admin_posts")
    else:
        form = AddPostForm()

    return render(request, "admin/add_post.html", {"form": form})


def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        form = EditPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect(
                "admin_posts"
            )  # Redirect to the admin posts page after editing
    else:
        form = EditPostForm(instance=post)

    return render(request, "admin/edit_post.html", {"form": form, "post": post})


def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect("admin_posts")  # You can return a response or redirect as needed


def delete_selected_posts(request):
    if request.method == "POST":
        selected_ids = request.POST.getlist("selected_ids[]")  # Retrieve selected IDs

        # Validate selected IDs as UUIDs
        try:
            uuids = [uuid.UUID(id_) for id_ in selected_ids]
        except ValueError:
            return JsonResponse(
                {"message": "Invalid UUID format in selected IDs"}, status=400
            )

        # If the IDs are valid UUIDs, proceed with deletion
        posts_to_delete = Post.objects.filter(id__in=uuids)
        posts_to_delete.delete()
        return JsonResponse(
            {"message": "Selected posts deleted successfully"}, status=200
        )
    else:
        return JsonResponse({"message": "Invalid request method"}, status=400)


# def reported_posts(request):
#     admin = request.user

#     reported_posts = Post.objects.filter(reported_by_users__isnull=False)
#     reported_posts_count = Post.objects.filter(reported_by_users__isnull=False).count()

#     context = {
#         "admin_name": admin.name,
#         "admin_email": admin.email,
#         "admin_avatar": admin.avatar,
#         "reported_posts": reported_posts,
#         "reported_posts_count": reported_posts_count,
#     }
#     return render(request, "admin/reported_posts.html", context)


def reported_posts(request):
    admin = request.user

    # Annotate each post with the count of unique reports
    reported_posts = Post.objects.filter(reported_by_users__isnull=False).annotate(
        report_count=Count("reported_by_users", distinct=True)
    )

    context = {
        "admin_name": admin.name,
        "admin_email": admin.email,
        "admin_avatar": admin.avatar,
        "reported_posts": reported_posts,
        # If you want to keep a total count of unique reports across all posts, update this:
        "reported_posts_count": reported_posts.aggregate(
            total_reports=Count("reported_by_users", distinct=True)
        )["total_reports"],
    }
    return render(request, "admin/reported_posts.html", context)


def post_create(request):
    body = request.data.get("body")

    if has_profanity(body):
        return Response({"error": "rawr found"}, status=400)


def delete_reported_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # Perform deletion of the post
    post.delete()
    return redirect("reported_posts")  # Redirect to a page after deletion


def remove_reports(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # Clear the reports for the post
    post.reported_by_users.clear()
    return redirect("reported_posts")  # Redirect to a page after removing reports


def beta_posts(request):
    admin = request.user

    context = {
        "admin_name": admin.name,
        "admin_email": admin.email,
        "admin_avatar": admin.avatar,
    }
    return render(request, "admin/beta.html", context)
