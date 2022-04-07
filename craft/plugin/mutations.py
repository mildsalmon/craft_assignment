import graphene
import graphql_jwt

from django.contrib.auth import get_user_model

from .decorators import token_auth

from graphql_jwt import mixins
from graphql_jwt.mutations import Verify
from graphql_jwt.mutations import Refresh

__all__ = [
    'ObtainJSONWebToken',
    'Verify',
    'Refresh',
]


class ObtainJSONWebToken(
    mixins.ResolveMixin,
    graphql_jwt.JSONWebTokenMutation
):
    @classmethod
    def Field(cls, *args, **kwargs):
        cls._meta.arguments.update({
            get_user_model().EMAIL_FIELD: graphene.String(required=True),
            'password': graphene.String(required=True),
        })
        return super(graphql_jwt.JSONWebTokenMutation, cls).Field(*args, **kwargs)

    @classmethod
    @token_auth
    def mutate(cls, root, info, **kwargs):
        return cls.resolve(root, info, **kwargs)

