from django.contrib import admin
from .models import Post, Comment,ContactUs,Profile, PostView
from blog.forms import PostAdminModelForm

class PostAdmin(admin.ModelAdmin):
    form = PostAdminModelForm
    list_display = ('post_id','title', 'slug', 'status','created_on','location','author',"state","views")
    list_filter = ("status","state","category","like",)
    search_fields = ['title', 'content','author',"category",]
    actions = ['approve_posts']

    def approve_posts(self, request, queryset):
        queryset.update(status=1)
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