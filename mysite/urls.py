"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap
from blog import views
from ckeditor_uploader import views as uploader_views
from django.views.decorators.cache import never_cache
sitemaps = {
    "posts": PostSitemap,
}

admin.site.site_header= "Tales BY Travellers"
admin.site.site_title= "TBT Admin "
admin.site.index_title= "Admin Panel"

urlpatterns = [
    # path('accounts/login', TemplateView.as_view(template_name="registration/login.html")),
    path('admin/', admin.site.urls),
    path("", include(('blog.urls', 'blog'), namespace="blog")),
    path('accounts/', include('django.contrib.auth.urls')),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^ckeditor/upload/', uploader_views.upload, name='ckeditor_upload'),
    url(r'^ckeditor/browse/', never_cache(uploader_views.browse), name='ckeditor_browse'),
    


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)