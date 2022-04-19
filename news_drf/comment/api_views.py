from rest_framework import viewsets
from .models import Comment
from .serializers import CommentSerializers


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers
