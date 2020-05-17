from .models import Comment,Post
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

class BlogForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('author', 'email', 'title','cover','location','state_choice','content')