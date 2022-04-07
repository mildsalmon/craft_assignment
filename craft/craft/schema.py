import graphene
# import graphql_jwt
from plugin import mutations

import plugin.schema as schema

class Query(schema.Query, graphene.ObjectType):
    pass


class Mutation(schema.Mutation, graphene.ObjectType):
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.Verify.Field()
    refresh_token = mutations.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)