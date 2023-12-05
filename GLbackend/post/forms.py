from django import forms
from .models import Post, PostAttachment, GameTitle


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["body", "game_title"]

    # menu = forms.ChoiceField(choices=Post.MENU_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "body",
            "game_title",
            "is_private",
            "menu",
        ]  # Fields to be edited by admin

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[
            "game_title"
        ].queryset = (
            GameTitle.objects.all()
        )  # Set the queryset for the game_title field
        self.fields["game_title"].widget = forms.Select(
            choices=GameTitle.objects.all().values_list("id", "title")
        )


class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["game_title", "is_private", "menu"]  # Fields to be edited by admin

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[
            "game_title"
        ].queryset = (
            GameTitle.objects.all()
        )  # Set the queryset for the game_title field
        self.fields["game_title"].widget = forms.Select(
            choices=GameTitle.objects.all().values_list("id", "title")
        )


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = PostAttachment
        fields = ("image",)
