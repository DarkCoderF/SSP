from django.contrib import admin

# Register your models here.
from .models import Posts, Tag, Comment

admin.site.register(Posts)
admin.site.register(Tag)
admin.site.register(Comment)