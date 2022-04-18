import graphene
from accounts.schema import AccountsQuery,AccountsMutation
from news.schema import NewsQuery,NewsMutation
from comment.schema import CommentQuery,CommentMutaion

class Query(AccountsQuery,
            NewsQuery,
            CommentQuery,
            graphene.ObjectType):
    pass

class Mutation(AccountsMutation,
                NewsMutation,
                CommentMutaion,
               graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query,mutation=Mutation)