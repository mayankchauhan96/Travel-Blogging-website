from .models import Comment,Post
from django import forms
from djrichtextfield.widgets import RichTextWidget


class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=RichTextWidget())
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

class BlogForm(forms.ModelForm):
    content = forms.CharField(widget=RichTextWidget())
    class Meta:
        model = Post
        fields = ('author', 'email', 'title','cover','location','state_choice','content','category')