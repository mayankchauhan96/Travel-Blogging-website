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
from sorl.thumbnail import ImageField


STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

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

STATE_CHOICES = (
    ("Somewhere In India","Somewhere In India"),
    ("Out Of India","Out Of India"),
    ("Andhra Pradesh","Andhra Pradesh"),
    ("Arunachal Pradesh","Arunachal Pradesh"),
    ("Assam","Assam"),
    ("Bihar","Bihar"),
    ("Chhattisgarh","Chhattisgarh"),
    ("Chandigarh","Chandigarh"),
    ("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),
    ("Daman and Diu","Daman and Diu"),
    ("Delhi","Delhi"),
    ("Goa","Goa"),
    ("Gujarat","Gujarat"),
    ("Haryana","Haryana"),
    ("Himachal Pradesh","Himachal Pradesh"),
    ("Jammu and Kashmir","Jammu and Kashmir"),
    ("Jharkhand","Jharkhand"),
    ("Karnataka","Karnataka"),
    ("Kerala","Kerala"),
    ("Madhya Pradesh","Madhya Pradesh"),
    ("Maharashtra","Maharashtra"),
    ("Manipur","Manipur"),
    ("Meghalaya","Meghalaya"),
    ("Mizoram","Mizoram"),
    ("Nagaland","Nagaland"),
    ("Orissa","Orissa"),
    ("Punjab","Punjab"),
    ("Pondicherry","Pondicherry"),
    ("Rajasthan","Rajasthan"),
    ("Sikkim","Sikkim"),
    ("Tamil Nadu","Tamil Nadu"),
    ("Tripura","Tripura"),
    ("Uttar Pradesh","Uttar Pradesh"),
    ("Uttarakhand","Uttarakhand"),
    ("West Bengal","West Bengal"),

)

class Category(models.Model):

    category = models.CharField(max_length=100, blank=True, null=True, choices=CATEGORY)

    def __str__(self):
        return self.category

class Post(models.Model):
    post_id = models.AutoField
    title = models.CharField(max_length=200, unique=True)
    slug = AutoSlugField(populate_from='title')
    cover = ImageField(upload_to='images/', null = True, blank= True,)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name= "posts")
    updated_on = models.DateTimeField(auto_now= True)
    content = RichTextField(blank = True , null= True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    state = models.CharField(max_length=80,choices=STATE_CHOICES)
    slug_st = AutoSlugField(populate_from='state')
    location = models.CharField(max_length=200)
    slug_lc = AutoSlugField(populate_from='location')
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
    bio = models.CharField(max_length=100, blank=True, null=True)
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