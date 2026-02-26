from django.db import models
from tinymce.models import HTMLField

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    url = models.SlugField(unique=True)
    meta_title = models.CharField(max_length=300)
    meta_description = models.TextField()
    thumbnail = models.ImageField(upload_to='blog/thumbnails')
    author = models.CharField(max_length=100)
    author_image = models.ImageField(upload_to='blog/authors/')
    content = HTMLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
