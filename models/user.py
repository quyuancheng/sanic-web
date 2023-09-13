from typing import Any, Dict, Tuple, Union

from tortoise import Model, fields
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash


class User(Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=100)
    name = fields.CharField(max_length=100, unique=True)
    password = fields.TextField()
    active = fields.BooleanField(default=True)

    class Meta:
        table = 'users'

    def __str__(self):
        return f"this is {self.name} table"
    # 这种经常用的 可以抽象出来让所有的模型可以用
    def to_dict(self) -> Dict[str, Union[datetime, int, str]]:
        rv = {f: getattr(self, f) for f in self._meta.fields}
        rv.pop("password")
        return rv


class GithubUser(Model):
    gid = fields.IntField(unique=True)
    email = fields.CharField(max_length=100, default='', unique=True)
    username = fields.CharField(max_length=100, unique=True)
    picture = fields.CharField(max_length=100, default='')
    link = fields.CharField(max_length=100, default='')

    class Meta:
        table = 'github_users'

    def to_dict(self) -> Dict[str, Union[datetime, int, str]]:
        rv = {f: getattr(self, f) for f in self._meta.fields}
        rv.pop("created_at")
        return rv


def generate_password(password: str) -> str:
    return generate_password_hash(
        password, method='pbkdf2:sha256')


async def create_user(**data) -> User:
    if 'name' not in data or 'password' not in data:
        raise ValueError('username and password are required.')

    data['password'] = generate_password(data.pop('password'))

    user = await User.create(**data)
    return user


async def validate_login(name: str, password: str) -> Tuple[bool, Union[User, None]]:
    if not (user := await User.filter(name=name).first()):
        return False, None
    if check_password_hash(user.password, password):
        return True, user
    return False, User()


async def create_github_user(user_info) -> GithubUser:
    user = await GithubUser.filter(gid=user_info.id).first()
    kwargs = {
        'gid': user_info.id,
        'link': user_info.link,
        'picture': user_info.picture,
        'username': user_info.username,
        'email': user_info.email or user_info.username,
    }
    user = await (user.update(**kwargs) if user
                  else GithubUser.create(**kwargs))
    return user
