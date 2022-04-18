from django.db import models
from django.conf import settings

# Create your models here.
class Article(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=25)
    choice1 = models.TextField()
    choice2 = models.TextField()


CHOICES = [
    ('B', 'Blue'),
    ('R', 'Red'), 
]

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    choice = models.CharField(max_length=30, choices=CHOICES)
    content = models.CharField(max_length=200)