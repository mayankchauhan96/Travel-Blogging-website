from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from autoslug import AutoSlugField
from django.utils import timezone
from django.urls import reverse
import json
import datetime
from ckeditor.fields import RichTextField


STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

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

STATE_CHOICES = (
    ("II","Somewhere In India"),
    ("OI","Out Of India"),
    ("AP","Andhra Pradesh"),
    ("AR","Arunachal Pradesh"),
    ("AS","Assam"),
    ("BR","Bihar"),
    ("CT","Chhattisgarh"),
    ("CH","Chandigarh"),
    ("DN","Dadra and Nagar Haveli"),
    ("DD","Daman and Diu"),
    ("DL","Delhi"),
    ("GA","Goa"),
    ("GJ","Gujarat"),
    ("HR","Haryana"),
    ("HP","Himachal Pradesh"),
    ("JK","Jammu and Kashmir"),
    ("JH","Jharkhand"),
    ("KA","Karnataka"),
    ("KL","Kerala"),
    ("MP","Madhya Pradesh"),
    ("MH","Maharashtra"),
    ("MN","Manipur"),
    ("ML","Meghalaya"),
    ("MZ","Mizoram"),
    ("NL","Nagaland"),
    ("OR","Orissa"),
    ("PB","Punjab"),
    ("PY","Pondicherry"),
    ("RJ","Rajasthan"),
    ("SK","Sikkim"),
    ("TN","Tamil Nadu"),
    ("TR","Tripura"),
    ("UP","Uttar Pradesh"),
    ("UK","Uttarakhand"),
    ("WB","West Bengal"),
)

class Category(models.Model):

    category = models.CharField(max_length=100, blank=True, null=True, choices=CATEGORY)

    def __str__(self):
        return self.category

class Post(models.Model):
    post_id = models.AutoField
    title = models.CharField(max_length=200, unique=True)
    slug = AutoSlugField(populate_from='title')
    cover = models.ImageField(upload_to='images/', null = True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name= "posts")
    updated_on = models.DateTimeField(auto_now= True)
    content = RichTextField(max_length=2000, blank = True , null= True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    state = models.CharField(max_length=80,choices=STATE_CHOICES)
    location = models.CharField(max_length=200)
    category = models.ManyToManyField(Category, blank = True, related_name="posts" )
    views = models.IntegerField(default= 0)
    like = models.ManyToManyField('auth.User', blank= True, related_name="post_liked")

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('home')

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"slug": self.slug})

    def get_like_url(self):
        return reverse("blog:like-toggle", kwargs={"slug": self.slug})

    def get_api_like_url(self):
        return reverse("blog:like-api-toggle", kwargs={"slug": self.slug})

class PostView(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='post_views')
    ip = models.CharField(max_length=40)
    session = models.CharField(max_length=40)
    created = models.DateTimeField(default=datetime.datetime.now())


class Comment(models.Model):

    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField(max_length=100)
    body = models.TextField(max_length=80)
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)


class ContactUs(models.Model):
    sno = models.AutoField
    name = models.CharField(max_length=80)
    email = models.EmailField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=500)

    class Meta:
        ordering = ['-created_on']

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=150)
    signup_confirmation = models.BooleanField(default=False)
    facebook_link = models.CharField(max_length=100, blank=True, null=True)
    instagram_link = models.CharField(max_length=100, blank=True, null=True)
    bio = models.CharField(max_length=400, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    Website = models.CharField(max_length=100, blank=True, null=True)
    youtube_channel = models.CharField(max_length=100, blank=True, null=True)


    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()