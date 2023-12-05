from django.urls import path

from . import api, views

urlpatterns = [
    path("discussion_posts/", api.discussion_posts, name="discussion_posts"),
    path("<uuid:pk>/", api.post_detail, name="post_detail"),
    path("<uuid:pk>/like/", api.post_like, name="post_like"),
    # path('<uuid:pk>/unlike/', api.post_unlike, name='post_unlike'),
    path("<uuid:pk>/comment/", api.post_create_comment, name="post_create_comment"),
    path("<uuid:pk>/delete/", api.post_delete, name="post_delete"),
    path("<uuid:pk>/report/", api.post_report, name="post_report"),
    path("profile/<uuid:id>/", api.post_list_profile, name="post_list_profile"),
    path("create/", api.post_create, name="post_create"),
    path("get_gametitle/", api.get_gametitle, name="get_gametitle"),
    # path('delete_post/', api.delete_post, name='delete_post'),
    path(
        "profile/<uuid:user_id>/post_count/",
        api.get_user_post_count,
        name="user_post_count",
    ),
    path(
        "profile/<uuid:user_id>/charisma_score/",
        api.get_charisma_score,
        name="get_charisma_score",
    ),
    path("marketplace_posts/", api.marketplace_posts, name="marketplace_posts"),
    path("connect_posts/", api.connect_posts, name="connect_posts"),
    path("tournament_posts/", api.tournament_posts, name="tournament_posts"),
    path("beta_posts/", api.beta_posts, name="beta_posts"),
    path("popular_games/", api.popular_games_endpoint, name="popular_games_endpoint"),
    # admin
    path("gl-posts/", views.admin_posts, name="admin_posts"),
    path("gl-posts/add", views.add_post, name="add_post"),
    path("gl-posts/edit/<uuid:post_id>/", views.edit_post, name="edit_post"),
    path("gl-posts/delete/<uuid:post_id>/", views.delete_post, name="delete_post"),
    path(
        "gl-posts/delete_selected_posts/",
        views.delete_selected_posts,
        name="delete_selected_posts",
    ),
    path("gl-posts/reported", views.reported_posts, name="reported_posts"),
    path(
        "gl-posts/reported/delete/<uuid:post_id>/",
        views.delete_reported_post,
        name="delete_reported_post",
    ),
    path(
        "gl-posts/reported/remove_reports/<uuid:post_id>/",
        views.remove_reports,
        name="remove_reports",
    ),
    path("gl-posts/beta-testing", views.beta_posts, name="beta_posts"),
]
