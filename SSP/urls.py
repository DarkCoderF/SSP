from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from .views import posts
from articles.sitemaps import BlogSitemap
from django.contrib.sitemaps.views import sitemap


sitemaps = {
    'blog': BlogSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('articles/' , include('articles.urls')),
    path('accounts/',include('accounts.urls')),
    path('', posts),
    path('ckeditor/',include('ckeditor_uploader.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},name='django.contrib.sitemaps.views.sitemap')
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)