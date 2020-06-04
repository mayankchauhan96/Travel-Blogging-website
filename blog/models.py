from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from autoslug import AutoSlugField
from django.utils import timezone
import json
from multiselectfield import MultiSelectField


STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

CATEGORY= (
    ("BE","Beaches"),
    ("IL","Islands"),
    ("HI","Hiking"),
    ("CA","Camping"),
    ("MT","Mountains"),
    ("DE","Deserts"),
    ("FO","Forests"),
    ("HP","Historic Places"),
    ("MO","Monuments"),
    ("TE","Temples"),
    ("MU","Museums"),
    ("ZO","Zoos"),
    ("TP","Theme Parks"),
    ("GA","Gardens"),
    ("AQ","Aquaria"),
    ("WC","Winter Carnival"),
    ("MA","Markets & Shopping"),
    ("UA","Urban"),
    ("RU","Rural"),
    ("RL","Rivers & Lakes"),
    ("CF","Couples Friendly"),
    ("ST","Sports Tourism"),
    ("JF","Just for Food "),
    ("RE","Resorts"),
    ("CU","Culture"),
    ("AD","Adventure"),
)

STATE_CHOICES = (
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


class Post(models.Model):
    post_id = models.AutoField
    title = models.CharField(max_length=200, unique=True)
    slug = AutoSlugField(populate_from='title')
    cover = models.ImageField(upload_to='images/', null = True)
    # author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_posts')
    author = models.CharField(max_length=80)
    updated_on = models.DateTimeField(auto_now= True)
    content = models.CharField(max_length=80)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    state_choice = models.CharField(max_length=80,choices=STATE_CHOICES)
    location = models.CharField(max_length=80)
    email = models.EmailField()
    category =MultiSelectField(choices=CATEGORY, max_choices= 4, blank=True, null=True )

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.CharField(max_length=80)
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

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
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150)
    signup_confirmation = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()