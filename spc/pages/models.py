from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    title = models.CharField(default='منشور عام', max_length=50)
    content = models.TextField()
    dateTime = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-dateTime']

class PostImage(models.Model):
    postID = models.ForeignKey(Post, on_delete=models.CASCADE)
    images = models.FileField(upload_to='postImages/')
 
    def __str__(self):
        return self.postID.title

class Comment(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    postID = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    updated = models.BooleanField(default=False)
    dateTime = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.userID.username + ' >> ' + self.postID.title + ' (' + self.comment + ')'

    class Meta:
        ordering = ['-dateTime']
