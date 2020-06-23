from .models import Comment,Post,ContactUs,Profile
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.apps import apps


CATEGORY= (
    ("Beaches","Beaches"),
    ("Islands","Islands"),
    ("Hiking","Hiking"),
    ("Camping","Camping"),
    ("Mountains","Mountains"),
    ("Deserts","Deserts"),
    ("Forests","Forests"),
    ("Historic","Historic"),
    ("Monuments","Monuments"),
    ("Temples","Temples"),
    ("Museums","Museums"),
    ("Zoos","Zoos"),
    ("ThemeParks","ThemeParks"),
    ("Gardens","Gardens"),
    ("Aquaria","Aquaria"),
    ("Winter","Winter"),
    ("Market","Market"),
    ("Urban","Urban"),
    ("Rural","Rural"),
    ("Rivers","Rivers"),
    ("Lakes","Lakes"),
    ("Couple","Couple"),
    ("Sports","Sports"),
    ("Food","Food "),
    ("Resorts","Resorts"),
    ("Culture","Culture"),
    ("Adventure","Adventure"),
    ("MotoBlogs","MotoBlogs"),
    ("Solo","Solo"),
    ("Summer","Summer"),
    ("TravelTips","TravelTips"),
)


class PostAdminModelForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = "__all__"

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

class BlogForm(forms.ModelForm):
    category = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple,
    choices=CATEGORY)
    location = forms.CharField(max_length=200, help_text='Location of the place you Visited')
    cover = forms.ImageField(help_text='Image size must be under 20MB | Keep it landscaped for better view')
    class Meta:
        model = Post
        fields = ('title','cover','location','state','content','category')

class EditForm(forms.ModelForm):
    location = forms.CharField(max_length=200, help_text='Location of the place you Visited')
    cover = forms.ImageField(help_text='Image size mus be under 20MB | Must be landscaped for better view')
    class Meta:
        model = Post
        fields = ('title','cover','location','state','content')

class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ('name', 'email', 'content')


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Enter your working Email Id')
    username = forms.CharField(max_length=60, help_text='It will be displayed on your BlogPost.')

    class Meta:
        model = User
        fields = ('username','email', 'password1', 'password2', )
    def __str__(self):
        return self.Email

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ( 'facebook_link','instagram_link','bio','city','Website','youtube_channel')

