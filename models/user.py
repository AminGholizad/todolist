from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from passlib.hash import bcrypt_sha256
from config.exceptions import UNAUTHORIZED

from models.base import Base, resolve_relationships, to_optional
from models.todo import Todo


class User(Base):
    name = fields.CharField(max_length=200)
    username = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=256)
    todolist: fields.ReverseRelation['Todo']

    @classmethod
    async def authenticate_user(cls, username: str, password: str):
        user = await cls.get(username=username)
        if not user:
            raise UNAUTHORIZED
        if not bcrypt_sha256.verify(password, user.password):
            raise UNAUTHORIZED
        return user


resolve_relationships()
UserPydantic = pydantic_model_creator(User, name='User')
UserPostPydantic = pydantic_model_creator(
    User, name='UserIn', exclude_readonly=True)
UserPutPydantic = to_optional(pydantic_model_creator(
    User, name='PartialUserIn', exclude_readonly=True))
