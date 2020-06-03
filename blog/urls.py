from . import views
from django.urls import path
from django.conf.urls import url

urlpatterns = [
    # path('', views.PostList.as_view(), name='home'),
    path('about_us/',  views.about_us, name='about_us'),
    path('contact_us/',  views.contact_us, name='contact_us'),
    path('search/',  views.search, name='search'),
    path('blog_form/',  views.blog_form, name='blog_form'),
    path('recent_post/',  views.PostInfiniteRecent.as_view(), name='recent_posts'),
    path('signup/', views.signup_view, name="signup"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('sent/', views.activation_sent_view, name="activation_sent"),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    path('', views.recent_post, name='home'),
    path('<slug:slug>/',  views.post_detail, name='post_detail'),

]