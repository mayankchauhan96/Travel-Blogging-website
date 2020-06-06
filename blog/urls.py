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
    path('', views.recent_post, name='home'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    url(r'^user/(?P<user_id>\d+)/update_profile/$', views.update_profile, name='update_profile'),
    url(r'^user/(?P<user_id>\d+)/myprofile/$', views.userprofileposts, name='user_url'),
    url(r'profile/(?P<user_id>\d+)/$', views.get_user_profile, name= "get_user_profile"),
    path('<slug:slug>/',  views.post_detail, name='post_detail'),
]