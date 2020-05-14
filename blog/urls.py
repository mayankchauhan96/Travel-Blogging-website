from . import views
from django.urls import path
from django.conf.urls import url

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('about_us/',  views.about_us, name='about_us'),
    path('blog_form/',  views.blog_form, name='blog_form'),
    path('<slug:slug>/',  views.post_detail, name='post_detail'),

]