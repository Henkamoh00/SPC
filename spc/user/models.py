from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from PIL import Image

# Create your models here.


# models.Model --> AbstructBaseUser --> AbstructUser --> User

class Profile(models.Model):
    gend = [
        ('ذكر','male'),
        ('انثى','female'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='defaults/defaultProfileImg.png', upload_to='profileImages/')
    phoneNumber = models.CharField(default='', max_length=15, blank=True)
    gender = models.CharField(default='male', max_length=5, choices=gend, blank=True)
    address = models.CharField(default='', max_length=200, blank=True)
    status = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.width > 240 or img.height > 240:
                img.thumbnail((240, 240))
                img.save(self.image.path)




class Concern(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.CharField(default='', max_length=200)
    email = models.CharField(max_length=50)
    fullName= models.CharField(default='client', max_length=50)
    content = models.TextField()
    dateTime = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.subject+ ' >> ' + self.email + ' (' + str(self.dateTime) + ')'

    class Meta:
        ordering = ['-dateTime']