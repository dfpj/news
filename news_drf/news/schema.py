from graphene_django.types import DjangoObjectType
import graphene
from .models import News, Author, Tag
from django.db import transaction
from graphql_jwt.decorators import login_required



class AuthorType(DjangoObjectType):
    class Meta:
        model = Author
        fields = ('user',)


class TagType(DjangoObjectType):
    class Meta:
        model = Tag
        fields = ('name',)


class TagInput(graphene.InputObjectType):
    name = graphene.String(required=True)


class NewsType(DjangoObjectType):
    class Meta:
        model = News
        fields = ('title', 'slug', 'text', 'view', 'id', 'tags', 'created', 'published', 'author')

class NewsInput(graphene.InputObjectType):
    title = graphene.String()
    slug = graphene.String()
    text = graphene.String()
    tags = graphene.List(TagInput)
    published = graphene.DateTime()


class NewsQuery(graphene.ObjectType):
    news = graphene.Field(NewsType, id=graphene.Int())
    full_news = graphene.List(NewsType)

    def resolve_full_news(selparent, info, **kwargsf):
        return News.objects.all()

    def resolve_news(parent, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            try:
                news = News.objects.get(id=id)
                news.view += 1
                news.save()
                return news
            except News.DoesNotExist:
                return None
        return None


class CreateNews(graphene.Mutation):
    news = graphene.Field(NewsType)
    ok = graphene.Boolean(default_value=False)

    class Arguments:
        input = NewsInput(required=True)

    @staticmethod
    @login_required
    def mutate(parent, info, input):
        try:
            author = Author.objects.get(user=info.context.user)
            # format dateTime : "2022-04-18T10:52:21+00:00"
            news = News.objects.create(title=input['title'],slug=input['slug'],text=input['text'],
                                       published=input['published'],author=author)
            with transaction.atomic():
                for dict_tag in input.get('tags'):
                    tag = Tag.objects.get_or_create(name=dict_tag.get('name'))[0]
                    news.tags.add(tag)
            return CreateNews(news=news, ok=True)
        except Author.DoesNotExist:
            return CreateNews(ok=False)


class MakeAuthor(graphene.Mutation):
    ok = graphene.Boolean(default_value=False)

    class Arguments:
        email = graphene.String(required=True)

    @staticmethod
    @login_required
    def mutate(parent, info, **kwargs):
        if kwargs.get('email') == info.context.user.email:
            Author.objects.get_or_create(user=info.context.user)
            return MakeAuthor(ok=True)
        return MakeAuthor(ok=False)

class UpdateNews(graphene.Mutation):
    news = graphene.Field(NewsType)
    ok = graphene.Boolean(default_value=False)

    class Arguments:
        id = graphene.Int()
        input = NewsInput()

    @staticmethod
    @login_required
    def mutate(parent, info,id,input):
        try:
            news = News.objects.get(id=id)
            if news.author.user == info.context.user:
                news.title = input.get('title') if input.get('title') else news.title
                news.slug =input.get('slug') if input.get('slug') else news.slug
                news.text =input.get('text') if input.get('text') else news.text
                # format dateTime : "2022-04-18T10:52:21+00:00"
                news.published = input.get('published') if input.get('published') else news.published
                if input.get('tags'):
                    with transaction.atomic():
                        news.tags.remove()
                        for dict_tag in input.get('tags'):
                            tag = Tag.objects.get_or_create(name=dict_tag.get('name'))[0]
                            news.tags.add(tag)
                news.save()
            return MakeAuthor(ok=True)
        except News.DoesNotExist:
            return MakeAuthor(ok=False)


class NewsMutation(graphene.ObjectType):
    create_news = CreateNews.Field()
    update_news =UpdateNews.Field()
    make_author = MakeAuthor.Field()

