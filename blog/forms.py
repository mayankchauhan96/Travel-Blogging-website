from .models import Comment,Post,ContactUs,Profile
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.apps import apps

CATEGORY= (
    ("Beaches ","Beaches"),
    ("Islands ","Islands"),
    ("Hiking","Hiking"),
    ("Camping ","Camping"),
    ("Mountains ","Mountains"),
    ("Deserts ","Deserts"),
    ("Forests ","Forests"),
    ("Historic Places ","Historic Places"),
    ("Monuments ","Monuments"),
    ("Temples ","Temples"),
    ("Museums ","Museums"),
    ("Zoos ","Zoos"),
    ("Theme Parks ","Theme Parks"),
    ("Gardens ","Gardens"),
    ("Aquaria ","Aquaria"),
    ("Winter ","Winter Carnival"),
    ("Markets & Shopping ","Markets & Shopping"),
    ("Urban ","Urban"),
    ("Rural ","Rural"),
    ("Rivers & Lakes ","Rivers & Lakes"),
    ("Couples Friendly ","Couples Friendly"),
    ("Sports Tourism ","Sports Tourism"),
    ("Just for Food ","Just for Food "),
    ("Resorts ","Resorts"),
    ("Culture ","Culture"),
    ("Adventure ","Adventure"),
    ("Moto Blogs ","Moto Blogs"),
    ("Solo ","Solo Travel"),
    ("Summer ","Summer Special"),
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
    location = forms.CharField(max_length=200, help_text='Place you Visited')

    class Meta:
        model = Post
        fields = ('title','cover','location','state','content','category')

class EditForm(forms.ModelForm):
    # category = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple,
    # choices=CATEGORY)
    location = forms.CharField(max_length=200, help_text='Place you Visited')

    class Meta:
        model = Post
        fields = ('title','cover','location','state','content')

class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ('name', 'email', 'content')


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=150, help_text='Enter your working Email Id')
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
        fields = ( 'facebook_link','instagram_link','bio','city','Website',)

