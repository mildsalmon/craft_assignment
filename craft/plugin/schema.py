from django.contrib.auth import get_user_model

import graphene
from graphene_django import DjangoObjectType

import logging

logger = logging.getLogger('query')


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, password, email):
        user = get_user_model()(
            email=email,
            username=email.split('@')[0],
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)


class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    users = graphene.List(UserType)

    def resolve_users(self, info):
        return get_user_model().objects.all()

    def resolve_me(self, info):
        user = info.context.user

        try:
            if user.is_anonymous:
                raise Exception("Not logged in!")
        except Exception as e:
            logger.warning(e)
            raise

        return user


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()