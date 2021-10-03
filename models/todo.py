from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from models.base import Base, resolve_relationships, to_optional

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.user import User


class Todo(Base):
    name = fields.CharField(max_length=200)
    done = fields.BooleanField(default=False)
    user: fields.ForeignKeyRelation['User'] = fields.ForeignKeyField(
        model_name='models.User',
        related_name='todolist')


resolve_relationships()
TodoPydantic = pydantic_model_creator(Todo, name='Todo')
TodoPostPydantic = pydantic_model_creator(
    Todo, name='TodoIn', exclude_readonly=True, exclude=('user_id', 'done'))
TodoPutPydantic = to_optional(pydantic_model_creator(
    Todo, name='PartialTodoIn', exclude_readonly=True, exclude=('user_id',)))
