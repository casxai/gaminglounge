from django.core.exceptions import ValidationError
from django.db.models import Q, Count
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from sklearn import logger

from account.models import User, FriendshipRequest
from account.serializers import UserSerializer
from notification.utils import create_notification

from .best_profanity import has_profanity  # profcheck

from .forms import PostForm, AttachmentForm
from .models import Post, Like, Comment, GameTitle, Category
from .serializers import (
    PostSerializer,
    PostDetailSerializer,
    CommentSerializer,
    GameTitleSerializer,
)
from account.models import User


@api_view(["GET"])
def discussion_posts(request):
    # Extracting user preferences
    user_pref_titles = (
        request.user.pref_game_titles.split(",")
        if request.user.pref_game_titles
        else []
    )
    user_pref_titles = (
        [
            int(title_id.strip("[]"))
            for title_id in user_pref_titles
            if title_id.strip("[]")
        ]
        if user_pref_titles
        else []
    )

    user_pref_category = request.user.pref_game_category
    user_ids = [request.user.id]
    for user in request.user.friends.all():
        user_ids.append(user.id)
    # Query for posts based on user preferences and menu = discussions
    pref_posts = Post.objects.filter(
        is_private=False, menu="Discussions"
    )  # Filter by menu field here
    if user_pref_titles:
        pref_posts = pref_posts.filter(Q(game_title__id__in=user_pref_titles))
    elif user_pref_category:
        categories = user_pref_category.split(",")
        pref_posts = pref_posts.filter(
            Q(game_title__categories__game_category__in=categories)
        )

    # Ordering posts by likes count
    pref_posts = pref_posts.order_by("-likes_count")  # Most liked posts first

    # Query for posts from user's friends
    friend_posts = Post.objects.filter(
        created_by_id__in=user_ids,
        is_private=False,
        menu="Discussions",
        is_offensive=False,
    )

    own_posts = Post.objects.filter(
        created_by=request.user,
        is_private=False,
        menu="Discussions",
        is_offensive=False,
    )
    # Combine the results and sort them
    combined_posts = (
        (pref_posts | friend_posts | own_posts).distinct().order_by("-likes_count")
    )
    sorted_posts = sorted(combined_posts, key=lambda x: x.likes_count, reverse=True)
    # Apply pagination
    paginator = PageNumberPagination()
    paginator.page_size = 5  # Number of posts per page
    paginated_post = paginator.paginate_queryset(sorted_posts, request)

    # Serialize paginated posts
    serializer = PostSerializer(paginated_post, many=True)

    # Return paginated response
    return paginator.get_paginated_response(serializer.data)


@api_view(["GET"])
def marketplace_posts(request):
    # Extracting user preferences
    user_pref_titles = (
        request.user.pref_game_titles.split(",")
        if request.user.pref_game_titles
        else []
    )
    user_pref_titles = (
        [
            int(title_id.strip("[]"))
            for title_id in user_pref_titles
            if title_id.strip("[]")
        ]
        if user_pref_titles
        else []
    )

    user_pref_category = request.user.pref_game_category

    user_ids = [request.user.id]

    for user in request.user.friends.all():
        user_ids.append(user.id)

    # Query for posts based on user preferences and menu = Marketplace
    pref_posts = Post.objects.filter(
        is_private=False, menu="Marketplace"
    )  # Filter by menu field here

    if user_pref_titles:
        pref_posts = pref_posts.filter(Q(game_title__id__in=user_pref_titles))
    elif user_pref_category:
        categories = user_pref_category.split(",")
        pref_posts = pref_posts.filter(
            Q(game_title__categories__game_category__in=categories)
        )

    # Ordering posts by likes count
    pref_posts = pref_posts.order_by("-likes_count")  # Most liked posts first

    # Query for posts from user's friends
    friend_posts = Post.objects.filter(
        created_by_id__in=user_ids,
        is_private=False,
        is_offensive=False,
        menu="Marketplace",
    )

    own_posts = Post.objects.filter(
        created_by=request.user,
        is_private=False,
        is_offensive=False,
        menu="Marketplace",
    )

    # # Combine the results
    # combined_posts = (pref_posts | friend_posts | own_posts).distinct()
    # sorted_posts = sorted(combined_posts, key=lambda x: x.likes_count, reverse=True)

    # paginator = PageNumberPagination()
    # paginator.page_size = 3
    # paginated_post = paginator.paginate_queryset(sorted_posts, request)

    # serializer = PostSerializer(paginated_post, many=True)
    # return Response(serializer.data)
    # Combine the results and sort them
    combined_posts = (
        (pref_posts | friend_posts | own_posts).distinct().order_by("-likes_count")
    )
    sorted_posts = sorted(combined_posts, key=lambda x: x.likes_count, reverse=True)
    # Apply pagination
    paginator = PageNumberPagination()
    paginator.page_size = 5  # Number of posts per page
    paginated_post = paginator.paginate_queryset(sorted_posts, request)

    # Serialize paginated posts
    serializer = PostSerializer(paginated_post, many=True)

    # Return paginated response
    return paginator.get_paginated_response(serializer.data)


@api_view(["GET"])
def connect_posts(request):
    # Extracting user preferences
    user_pref_titles = (
        request.user.pref_game_titles.split(",")
        if request.user.pref_game_titles
        else []
    )
    user_pref_titles = (
        [
            int(title_id.strip("[]"))
            for title_id in user_pref_titles
            if title_id.strip("[]")
        ]
        if user_pref_titles
        else []
    )

    user_pref_category = request.user.pref_game_category

    user_ids = [request.user.id]

    for user in request.user.friends.all():
        user_ids.append(user.id)

    # Query for posts based on user preferences and menu = discussions
    pref_posts = Post.objects.filter(
        is_private=False, menu="Connect"
    )  # Filter by menu field here

    if user_pref_titles:
        pref_posts = pref_posts.filter(Q(game_title__id__in=user_pref_titles))
    elif user_pref_category:
        categories = user_pref_category.split(",")
        pref_posts = pref_posts.filter(
            Q(game_title__categories__game_category__in=categories)
        )

    # Ordering posts by likes count
    pref_posts = pref_posts.order_by("-likes_count")  # Most liked posts first

    # Query for posts from user's friends
    friend_posts = Post.objects.filter(
        created_by_id__in=user_ids, is_private=False, is_offensive=False, menu="Connect"
    )

    own_posts = Post.objects.filter(
        created_by=request.user,
        is_private=False,
        menu="Connect",
        is_offensive=False,
    )
    # Combine the results and sort them
    combined_posts = (
        (pref_posts | friend_posts | own_posts).distinct().order_by("-likes_count")
    )
    sorted_posts = sorted(combined_posts, key=lambda x: x.likes_count, reverse=True)
    # Apply pagination
    paginator = PageNumberPagination()
    paginator.page_size = 5 # Number of posts per page
    paginated_post = paginator.paginate_queryset(sorted_posts, request)

    # Serialize paginated posts
    serializer = PostSerializer(paginated_post, many=True)

    # Return paginated response
    return paginator.get_paginated_response(serializer.data)


@api_view(["GET"])
def tournament_posts(request):
     # Extracting user preferences
    user_pref_titles = (
        request.user.pref_game_titles.split(",")
        if request.user.pref_game_titles
        else []
    )
    user_pref_titles = (
        [
            int(title_id.strip("[]"))
            for title_id in user_pref_titles
            if title_id.strip("[]")
        ]
        if user_pref_titles
        else []
    )

    user_pref_category = request.user.pref_game_category

    user_ids = [request.user.id]

    for user in request.user.friends.all():
        user_ids.append(user.id)

    # Query for posts based on user preferences and menu = discussions
    pref_posts = Post.objects.filter(
        is_private=False, menu="Tournament"
    )  # Filter by menu field here

    if user_pref_titles:
        pref_posts = pref_posts.filter(Q(game_title__id__in=user_pref_titles))
    elif user_pref_category:
        categories = user_pref_category.split(",")
        pref_posts = pref_posts.filter(
            Q(game_title__categories__game_category__in=categories)
        )

    # Ordering posts by likes count
    pref_posts = pref_posts.order_by("-likes_count")  # Most liked posts first

    # Query for posts from user's friends
    friend_posts = Post.objects.filter(
        created_by_id__in=user_ids, is_private=False, is_offensive=False, menu="Tournament"
    )

    own_posts = Post.objects.filter(
        created_by=request.user,
        is_private=False,
        menu="Tournament",
        is_offensive=False,
    )
    # Combine the results and sort them
    combined_posts = (
        (pref_posts | friend_posts | own_posts).distinct().order_by("-likes_count")
    )
    sorted_posts = sorted(combined_posts, key=lambda x: x.likes_count, reverse=True)
    # Apply pagination
    paginator = PageNumberPagination()
    paginator.page_size = 5  # Number of posts per page
    paginated_post = paginator.paginate_queryset(sorted_posts, request)

    # Serialize paginated posts
    serializer = PostSerializer(paginated_post, many=True)

    # Return paginated response
    return paginator.get_paginated_response(serializer.data)


@api_view(["GET"])
def beta_posts(request):
    user_ids = [request.user.id]

    for user in request.user.friends.all():
        user_ids.append(user.id)

    # Query for posts based on user preferences and menu = beta testing
    pref_posts = Post.objects.filter(is_private=False, menu="Beta Testing")

    friend_posts = Post.objects.filter(
        created_by_id__in=user_ids,
        is_private=False,
        is_offensive=False,
        menu="Beta Testing",
    )

    own_posts = Post.objects.filter(
        created_by=request.user,
        is_private=False,
        is_offensive=False,
        menu="Beta Testing",
    )

    # Combine the results
    combined_posts = pref_posts | friend_posts

    # Combine the results and sort them
    combined_posts = (
        (pref_posts | friend_posts | own_posts).distinct().order_by("-likes_count")
    )
    sorted_posts = sorted(combined_posts, key=lambda x: x.likes_count, reverse=True)

    serializer = PostSerializer(sorted_posts, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def post_detail(request, pk):
    user_ids = [request.user.id]

    for user in request.user.friends.all():
        user_ids.append(user.id)

    post = Post.objects.filter(Q(created_by_id__in=user_ids) | Q(is_private=False)).get(
        pk=pk
    )

    serialized_data = PostDetailSerializer(post).data
    print(serialized_data)  # Check the console for the serialized data

    return JsonResponse({"post": serialized_data})


@api_view(["GET"])
def post_list_profile(request, id):
    user = User.objects.get(pk=id)  # change later to feed only
    posts = Post.objects.filter(created_by_id=id)
    if not request.user in user.friends.all():
        posts = posts.filter(is_private=False, is_offensive=False)

    post_serializer = PostSerializer(posts, many=True)
    user_serializer = UserSerializer(user)

    can_send_friendship_request = True

    if request.user in user.friends.all():
        can_send_friendship_request = False

    check1 = FriendshipRequest.objects.filter(created_for=request.user).filter(
        created_by=user
    )
    check2 = FriendshipRequest.objects.filter(created_for=user).filter(
        created_by=request.user
    )

    if check1 or check2:
        can_send_friendship_request = False

    is_close_to_ban = user.calculate_charisma_score() <= -3 

    return JsonResponse(
        {
            "posts": post_serializer.data,
            "user": user_serializer.data,
            "can_send_friendship_request": can_send_friendship_request,
             "is_close_to_ban": is_close_to_ban,  # Include is_close_to_ban in the response
        },
        safe=False,
    )


@api_view(["POST"])
def post_create(request):
    form = PostForm(request.POST)
    attachment = None
    attachment_form = AttachmentForm(request.POST, request.FILES)
    body = request.data.get("body")  # profcheck\

    print(request.FILES)

    if attachment_form.is_valid():
        attachment = attachment_form.save(commit=False)
        attachment.created_by = request.user
        attachment.save()

    if form.is_valid():
        post = form.save(commit=False)  # commit false so it wont go through the backend
        post.created_by = request.user
        post.menu = request.data.get("menu")

        post.save()

        # Assuming 'game_title' is a valid field in your Post model
        game_title_id = request.POST.get("game_title")
        if game_title_id:
            # Assuming 'game_title' is a ForeignKey field in the Post model
            post.game_title_id = game_title_id
            post.save()

        if attachment:
            post.attachments.add(attachment)
            post.save()

        # to add in post count when user posts
        user = request.user
        user.posts_count = user.posts_count + 1
        user.save()

        if has_profanity(body):
            post.is_offensive = True
            post.save()

            return Response(
                {"error": "profanity detectedss"}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = PostSerializer(post)

        return JsonResponse(serializer.data, safe=False)
    else:
        print(form.errors)
        return JsonResponse({"error": "form not valid"}, status=400)


@api_view(["POST"])
def post_like(request, pk):
    post = Post.objects.get(pk=pk)

    if not post.likes.filter(created_by=request.user):
        like = Like.objects.create(created_by=request.user)

        post = Post.objects.get(pk=pk)
        post.likes_count = post.likes_count + 1
        post.likes.add(like)
        post.save()

        notification = create_notification(request, "post_like", post_id=post.id)

        return JsonResponse({"message": "like created"})
    else:
        return JsonResponse({"message": "post already like"})


@api_view(["POST"])
def post_create_comment(request, pk):
    comment = Comment.objects.create(
        body=request.data.get("body"), created_by=request.user
    )
    post = Post.objects.get(pk=pk)
    post.comments.add(comment)
    post.comments_count = post.comments_count + 1
    post.save()

    notification = create_notification(request, "post_comment", post_id=post.id)

    serializer = CommentSerializer(comment)
    return JsonResponse(serializer.data, safe=False)


@api_view(["DELETE"])
def post_delete(request, pk):
    # Retrieve the post to be deleted and its creator
    post = Post.objects.filter(created_by=request.user).get(pk=pk)
    user = post.created_by

    # Check if the post exists and if the user is the creator
    if post:
        if user == request.user:
            # Delete the post
            post.delete()

            # Update the user's post_count by subtracting 1
            user.posts_count -= 1
            user.save()

            return JsonResponse({"message": "Post deleted successfully"})
        else:
            return JsonResponse(
                {"error": "You do not have permission to delete this post"}, status=403
            )
    else:
        return JsonResponse({"error": "Post not found"}, status=404)


@api_view(["POST"])
def post_report(request, pk):
    post = Post.objects.get(pk=pk)
    post.reported_by_users.add(request.user)
    post.save()

    return JsonResponse({"message": "post reported"})


@api_view(["GET"])
def get_gametitle(request, *args, **kwargs):
    try:
        # Remove specific fields from the distinct call
        game_titles = GameTitle.objects.values("id", "title").distinct()
        return JsonResponse(list(game_titles), safe=False)
    except Exception as e:
        print(f"Error in get_gametitle view: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)


def get_user_post_count(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        post_count = user.posts_count
        return JsonResponse({"posts_count": post_count})
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)


def get_charisma_score(request, user_id):
    try:
        # Fetch the user instance
        user = User.objects.get(id=user_id)

        # Calculate the charisma score for the user
        charisma_score_count = user.calculate_charisma_score()
        user.ban_user()

        # Return JSON response with the charisma score
        return JsonResponse({"charisma_score_count": charisma_score_count})
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)


def get_popular_games():
    # Aggregate and annotate the count of related posts for each GameTitle
    popular_games = (
        GameTitle.objects.annotate(num_posts=Count("post"))
        .order_by("-num_posts")
        .values("title", "num_posts")[:5]  # Fetch top 5 GameTitles by post count
    )
    return popular_games


@api_view(["GET"])
def popular_games_endpoint(request):
    popular_games = get_popular_games()
    serialized_games = list(popular_games)
    return JsonResponse(serialized_games, safe=False)
