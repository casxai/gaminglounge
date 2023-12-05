from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import User


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("name", "email", "password1", "password2")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "name",
            "email",
            "bio",
            "avatar",
        )


class adminForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["email", "name"]  # Add other fields if required

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# edit admin form
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["name", "email", "avatar"]

    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        # Customize widgets or add extra field configurations if needed
        self.fields["avatar"].widget.attrs[
            "accept"
        ] = "image/*"  # Accept only image files


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_new_password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        user = self.user

        # Check if the old password matches the user's current password
        if not user.check_password(old_password):
            raise forms.ValidationError("The entered old password is incorrect.")

        return old_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_new_password = cleaned_data.get("confirm_new_password")

        if (
            new_password
            and confirm_new_password
            and new_password != confirm_new_password
        ):
            raise forms.ValidationError("New passwords don't match")

        return cleaned_data


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "name", "avatar", "is_active"]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "avatar": forms.FileInput(attrs={"class": "form-control-file"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
