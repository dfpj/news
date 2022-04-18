from django.db import models
from django.conf import settings
from news.models import News


class Comment(models.Model):
    writer = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    news = models.ForeignKey(News,on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]