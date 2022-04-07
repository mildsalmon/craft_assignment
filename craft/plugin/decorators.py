from functools import wraps

from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext as _

from promise import Promise, is_thenable

from graphql_jwt import exceptions
from graphql_jwt.refresh_token.shortcuts import refresh_token_lazy
from graphql_jwt.settings import jwt_settings
from graphql_jwt.shortcuts import get_token

__all__ = [
    'token_auth',
    'setup_jwt_cookie',
]


def token_auth(f):
    @wraps(f)
    @setup_jwt_cookie
    def wrapper(cls, root, info, password, **kwargs):
        def on_resolve(values):
            user, payload = values
            payload.token = get_token(user, info.context)

            if jwt_settings.JWT_LONG_RUNNING_REFRESH_TOKEN:
                payload.refresh_token = refresh_token_lazy(user)

            return payload

        email = kwargs.get(get_user_model().EMAIL_FIELD)
        username = email.split('@')[0]

        # 만약 authorization header에 json webtoken이 포함된 경우 경우
        # 주어진 json webtoken에 해당하는 email 값을 찾아 "이미 {email}로 로그인 하였습니다."라는 텍스트
        # 를 반환
        if info.context.user.is_authenticated:
            if str(info.context.user) != email:
                raise exceptions.JSONWebTokenError(
                    _(f"이미 {info.context.user}로 로그인 하셨습니다.")
                )

        user = authenticate(
            request=info.context,
            username=username,
            password=password,
            skip_jwt_backend=True)

        if user is None:
            raise exceptions.JSONWebTokenError(
                _('Please, enter valid credentials'))

        if hasattr(info.context, 'user'):
            info.context.user = user

        result = f(cls, root, info, **kwargs)
        values = (user, result)

        if is_thenable(result):
            return Promise.resolve(values).then(on_resolve)
        return on_resolve(values)
    return wrapper


def setup_jwt_cookie(f):
    @wraps(f)
    def wrapper(cls, root, info, *args, **kwargs):
        result = f(cls, root, info, **kwargs)

        if getattr(info.context, 'jwt_cookie', False):
            info.context.jwt = result.token
        return result
    return wrapper
