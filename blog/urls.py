from . import views
from django.urls import path, include
from django.conf.urls import url

urlpatterns = [
    # path('', views.PostList.as_view(), name='home'),
    path('about_us/',  views.about_us, name='about_us'),
    path('contact_us/',  views.contact_us, name='contact_us'),
    path('search/',  views.search, name='search'),
    path('blog_form/',  views.blog_form, name='blog_form'),
    path('recent_post/',  views.PostInfiniteRecent.as_view(), name='recent_posts'),

    #autharisation
    path('signup/', views.signup_view, name="signup"),
    path('accounts/login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('sent/', views.activation_sent_view, name="activation_sent"),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),

    path('', views.recent_post, name='home'),
    url(r'^user/(?P<user_id>\d+)/update_profile/$', views.update_profile, name='update_profile'),
    url(r'^user/(?P<user_id>\d+)/myprofile/$', views.userprofileposts, name='user_url'),
    url(r'profile/(?P<user_id>\d+)/$', views.get_user_profile, name= "get_user_profile"),
    url(r'category/(?P<category>\w+)/$', views.get_category, name= "get_category"),
    path('state/<slug:slug_st>', views.get_state, name= "get_state"),
    path('location/<slug:slug_lc>', views.get_location, name= "get_location"),
    path('<slug:slug>/',  views.post_detail, name='post_detail'),
    path('<slug:slug>/update',  views.post_update, name='post_update'),
    path('<slug:slug>/delete',  views.post_delete, name='post_delete'),

    path('<slug:slug>/like/',  views.PostLikeToggle.as_view(), name='like-toggle'),
    path('api/<slug:slug>/like/',  views.PostLikeAPIToggle.as_view(), name='like-api-toggle'),

]

app_name = "blog"