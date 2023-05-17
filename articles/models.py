from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from django.urls import reverse

class Article(models.Model):
    DRAFT = 'ذخیره'
    PUBLISH ='انتشار'

    STATUS_CHOICES = [
        (DRAFT, 'ذخیره'),
        (PUBLISH, 'ذخیره و انتشار'),
    ]

    title = models.CharField(max_length = 100)
    slug = models.SlugField()
    subheading = models.CharField(max_length=100, default="",verbose_name="توضیحات")
    tags = TaggableManager()
    body = RichTextUploadingField()
    date = models.DateTimeField(auto_now_add = True)
    image = models.ImageField(default='default.jpg',blank=True,upload_to='cover_images/')
    author = models.ForeignKey(User,default=None,on_delete=models.CASCADE,null=True)
    status = models.CharField(max_length=7, choices=STATUS_CHOICES, default=PUBLISH,verbose_name='وضعیت')
    def __str__(self):
        return self.title

    def snippet(self):
        return self.subheading[:50] + ' ...'
    
    def get_absolute_url(self):
        return reverse("articles:detail", kwargs={"slug": self.slug})