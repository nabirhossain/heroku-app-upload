from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):    
        return self.name

class post(models.Model):
    post_author = models.ForeignKey(author, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    post_body = models.TextField()
    post_image = models.FileField()
    post_category = models.ForeignKey(category, on_delete=models.CASCADE)
    posted_on = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self): 
        return self.post_title
