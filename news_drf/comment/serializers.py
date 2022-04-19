from rest_framework import serializers
from .models import Comment


class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields =('writer','news','text')