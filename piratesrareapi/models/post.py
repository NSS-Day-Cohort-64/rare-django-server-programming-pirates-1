"""Post model"""

from django.db import models

class Post(models.Model):
    author = models.ForeignKey("Author", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    publication_date = models.DateTimeField()
    image_url = models.CharField(max_length=500)
    content = models.CharField(max_length=1000)
    approved = models.BooleanField()
