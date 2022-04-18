from django.db import models
from django.conf import settings
from django.utils import timezone

class Gallery(models.Model):
    image = models.ImageField()

class Author(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)


class Tag(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class News(models.Model):
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    text = models.TextField()
    view = models.IntegerField(default=0)
    images = models.ManyToManyField(Gallery)
    author = models.ForeignKey(Author,on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    created = models.DateTimeField(auto_now_add=True)
    published = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title[:50]

    class Meta:
        verbose_name_plural ="News"