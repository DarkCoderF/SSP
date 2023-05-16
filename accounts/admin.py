from django.contrib import admin
from .models import UserInfo


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'about', 'photo', 'phone')
    list_filter = ('phone',)
    
admin.site.register(UserInfo, UserInfoAdmin)
