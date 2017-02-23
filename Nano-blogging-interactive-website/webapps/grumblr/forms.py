from django import forms

from grumblr.models import *
from django.contrib.auth.models import User


class EmailForm(forms.Form):
    email = forms.CharField(max_length=200, label='Email')


class PostForm(forms.Form):
    post = forms.CharField(max_length=200, label='Post')


class CommentForm(forms.Form):
    post = forms.CharField(max_length=200, label='Comment')


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=20, label='User name')
    first_name = forms.CharField(max_length=200, label='First name')
    last_name = forms.CharField(max_length=200, label='Last name')
    email1 = forms.CharField(max_length=200, label='Email')
    email2 = forms.CharField(max_length=200, label='Confirm Email')
    password1 = forms.CharField(max_length=200, label='Password', widget = forms.PasswordInput())
    password2 = forms.CharField(max_length=200, label='Confirm password', widget = forms.PasswordInput())

    def clean(self):

        cleaned_data = super(RegistrationForm, self).clean()

        email1 = cleaned_data.get('email1')
        email2 = cleaned_data.get('email2')
        if email1 and email2 and email1 != email2:
            raise forms.ValidationError("Email did not match.")

        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        return cleaned_data

    def clean_username(self):

        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        return username


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'follower', )
        widgets = {'picture': forms.FileInput()}
        # fields = ('first_name', 'last_name', ... etc.,)
