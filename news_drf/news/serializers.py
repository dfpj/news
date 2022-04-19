from rest_framework import serializers
from .models import Tag,Gallery,Author,News


class TagSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields =('name',)

class GallerySerializers(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields =('image',)

class AuthorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields =('user',)

class NewsSerializers(serializers.ModelSerializer):
    tags = TagSerializers(many=True,required=False)
    images = GallerySerializers(many=True,required=False)
    class Meta:
        model = News
        fields =('title','text','slug','author','tags','images','published')
        extra_kwargs ={
            'published':{'required':False}
        }