from django.urls import path
from . import views
from django.conf.urls import include

app_name = "articles"
urlpatterns = [
    path('', views.articles_list, name="list"),
    path('create',views.create_article, name = "create"),
    path('<slug>',views.PostDetail.as_view(), name= "detail"),
    path('tag/<slug:tag_slug>/',views.articles_list, name='post_tag'),
    path('tinymce',include('tinymce.urls'))
]
