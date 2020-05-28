from django.contrib import admin
from .models import Post, Comment,ContactUs

class PostAdmin(admin.ModelAdmin):
    list_display = ('post_id','title', 'slug', 'status','created_on','location','email','author',"state_choice","category",)
    list_filter = ("status","state_choice","category",)
    search_fields = ['title', 'content','author']
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