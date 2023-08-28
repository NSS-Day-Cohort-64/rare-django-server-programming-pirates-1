"""Comment model"""

from django.db import models

class Comment(models.Model):
    author = models.ForeignKey("Author", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    content = models.CharField(max_length=500)
    creation_date = models.DateTimeField()
