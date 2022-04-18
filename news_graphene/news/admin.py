from django.contrib import admin
from .models import News,Gallery,Author,Tag
# Register your models here.

admin.site.register(News)
admin.site.register(Gallery)
admin.site.register(Author)
admin.site.register(Tag)