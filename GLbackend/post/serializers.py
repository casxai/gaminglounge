from rest_framework import serializers

from account.serializers import UserSerializer

from .models import Post, PostAttachment, Comment, GameTitle


class PostAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostAttachment
        fields = (
            "id",
            "get_image",
        )


class GameTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameTitle
        fields = ["id", "title"]  # Adjust fields as needed


class PostSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    attachments = PostAttachmentSerializer(read_only=True, many=True)
    game_title = GameTitleSerializer(read_only=True)
    menu = serializers.CharField(read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "body",
            "is_private",
            "likes_count",
            "comments_count",
            "created_by",
            "created_at_formatted",
            "attachments",
            "game_title",
            "post_url",
            "menu",
        )


class CommentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            "id",
            "body",
            "created_by",
            "created_at_formatted",
        )


class PostDetailSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)
    attachments = PostAttachmentSerializer(read_only=True, many=True)
    game_title = GameTitleSerializer(read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "body",
            "likes_count",
            "comments_count",
            "created_by",
            "created_at_formatted",
            "comments",
            "attachments",
            "game_title",
            "post_url",
        )
