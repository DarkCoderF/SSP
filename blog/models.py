from django.db import models
import uuid
from users.models import Profile
from django.urls import reverse


class Posts(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    photo = models.ImageField(null = True, blank = True, default ="default.jpg")
    tags = models.ManyToManyField('Tag', blank="True")
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default = uuid.uuid4, unique=True, primary_key = True, editable=False)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['title','-created']

    @property
    def imageURL(self):
        try:
            url = self.photo.url
        except:
            url = ''
        return url
    def get_absolute_url(self):
        return reverse('post',args=[self.id])
    def get_comments(self):
        return self.comments.filter(parent=None).filter(active=True)

class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default = uuid.uuid4, unique=True, primary_key = True, editable=False)

    def __str__(self):
        return self.name


class Comment(models.Model):
    post = models.ForeignKey(Posts,on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=50)
    email = models.EmailField()
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return self.body

    def get_comments(self):
        return Comment.objects.filter(parent=self).filter(active=True)