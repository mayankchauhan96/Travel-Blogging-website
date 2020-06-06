from .models import Comment,Post,ContactUs,Profile
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

class BlogForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','cover','location','state_choice','content','category')

class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ('name', 'email', 'content')


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=150, help_text='Email')
    class Meta:
        model = User
        fields = ('username','email', 'password1', 'password2', )

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ( 'facebook_link','instagram_link','bio' )

