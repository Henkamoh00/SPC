from django.db import models

# Create your models here.

class About(models.Model):
    image = models.ImageField(default='../static/images/about.jpeg', upload_to='HomeImages/')
    text = models.TextField()



class Service(models.Model):
    image = models.ImageField(default='../static/images/service.jpeg', upload_to='HomeImages/')
    title = models.CharField(max_length=20)


class History(models.Model):
    image = models.ImageField(default='../static/images/achivement.jpeg', upload_to='HomeImages/')
    title = models.CharField(max_length=20)
    abstract = models.CharField(max_length=150)


class Team(models.Model):
    image = models.ImageField(default='../static/images/team.jpeg', upload_to='HomeImages/')
    emp_name = models.CharField(max_length=20)
    job_position = models.CharField(max_length=50)