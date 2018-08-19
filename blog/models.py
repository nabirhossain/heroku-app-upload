from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class author(models.Model):
    auth_name = models.ForeignKey(User, on_delete=models.CASCADE)
    auth_image = models.FileField()
    auth_details = models.TextField()

    def __str__(self): #  এডমিনে  আমরা   উক্ত  মডেলের  যে  ফিল্ডটিকে  শো  করাতে  চাই
        return self.auth_name.username

class category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):    #  এডমিনে  আমরা   উক্ত  মডেলের  যে  ফিল্ডটিকে  শো  করাতে  চাই
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

    def __str__(self): #  এডমিনে  আমরা   উক্ত  মডেলের  যে  ফিল্ডটিকে  শো  করাতে  চাই
        return self.post_title
