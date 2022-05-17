import datetime

from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    """
    Post model
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=20)
    text = models.TextField(max_length=140, blank=True)
    create_time = models.DateTimeField(default=datetime.datetime.now())

    class Meta:
        ordering = ('-create_time',)

    def __str__(self):
        return self.title
