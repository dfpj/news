from .models import Comment
from graphene_django.types import DjangoObjectType
import graphene
from news.models import News
from graphql_jwt.decorators import login_required


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment


class CommentQuery(graphene.ObjectType):
    comment = graphene.Field(CommentType, comment_id=graphene.Int(required=True))
    comments_one_news = graphene.List(CommentType, news_id=graphene.Int(required=True))

    def resolve_comment(selparent, info, **kwargs):
        try:
            comment = Comment.objects.get(id=kwargs.get('comment_id'))
            return comment
        except Comment.DoesNotExist:
            return None

    def resolve_comments_one_news(selparent, info, **kwargs):
        try:
            news = News.objects.get(id=kwargs.get('news_id'))
            return Comment.objects.filter(news=news)
        except News.DoesNotExist:
            return None


class CreateComment(graphene.Mutation):
    comment = graphene.Field(CommentType)
    ok = graphene.Boolean(default_value=False)

    class Arguments:
        news_id = graphene.Int(required=True)
        text = graphene.String(required=True)

    @staticmethod
    @login_required
    def mutate(parent, info, news_id, text):
        user = info.context.user
        try:
            news = News.objects.get(id=news_id)
            comment = Comment.objects.create(writer=user, news=news, text=text)
            return CreateComment(comment=comment, ok=True)
        except News.DoesNotExist:
            return None



class CommentMutaion(graphene.ObjectType):
    create_comment = CreateComment.Field()
