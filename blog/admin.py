from django.contrib import admin
from .models import Post, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status','created_on','location','email')
    list_filter = ("status","state_choice",)
    search_fields = ['title', 'content','author']
    prepopulated_fields = {'slug': ('title',)}
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