from django.contrib import admin
from .models import Post, Comment,ContactUs,Profile, PostView
from blog.forms import PostAdminModelForm
from mysite.settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail, send_mass_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.auth.models import User,auth
import random
from django.core.mail import get_connection, EmailMultiAlternatives



class PostAdmin(admin.ModelAdmin):
    form = PostAdminModelForm
    list_display = ('post_id','title', 'slug', 'status','created_on','location','author',"state","views")
    list_filter = ("status","state","category","location",)
    search_fields = ['title', 'location','author',"category",]
    actions = ['approve_posts']

    def approve_posts(self, request, queryset):
        current_site = get_current_site(request)
        subject = 'Congratulations! Your post is live now.'
        user = queryset.values("author_id")
        user = user[0]
        user = user["author_id"]
        slug = queryset.values("slug")
        slug = slug[0]
        slug = slug['slug']
        usr = User.objects.filter(id=user)
        usr = usr[0]
        email = usr.email
        username = usr.username
        # load a template like get_template() 
        # and calls its render() method immediately.
        message = render_to_string('registration/publish.html', {
            'user': username,
            'domain': current_site.domain,
            'slug': slug
        })
        recepient = email
        send_mail(subject, 
    message, DEFAULT_FROM_EMAIL, [recepient], fail_silently = False)

        title = queryset.values("title")
        title = title[0]
        title = title['title']
        subject = 'New blog is up: ' + title
        emails = []
        for i in User.objects.values_list('email',flat=True):
            emails.append(i)
        try:
            for i in Comment.objects.values_list('email',flat=True):
                if i not in emails:
                    emails.append(i)
        except:
            pass
        emails.remove(email)
        random.shuffle(emails)
        recepient = emails[:100]

        message = render_to_string('registration/publishall.html', {
            'user': username,
            'domain': current_site.domain,
            'slug': slug,
            'title':title
        })
        queryset.update(status=1)
        msg = EmailMultiAlternatives(subject, 
    message, DEFAULT_FROM_EMAIL, [recepient[0]], bcc=recepient)
        msg.send() 
    #     send_mail(subject, 
    # message, DEFAULT_FROM_EMAIL, recepient, fail_silently = False)

admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
admin.site.register(Comment, CommentAdmin)

class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('sno','name', 'email', 'content', 'created_on')
admin.site.register(ContactUs, ContactUsAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('email','facebook_link')
admin.site.register(Profile, ProfileAdmin)

class PostViewAdmin(admin.ModelAdmin):
    list_display = ('ip','session','created','post')
    list_filter = ('session',)

admin.site.register(PostView, PostViewAdmin)