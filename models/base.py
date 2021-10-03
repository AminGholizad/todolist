from tortoise import Tortoise, fields
from tortoise.models import Model
from tortoise.contrib.pydantic import PydanticModel


def to_optional(model: PydanticModel) -> PydanticModel:
    for field in model.__fields__.values():
        field.required = False

    return model


model_list = ["models.user", 'models.todo']


def resolve_relationships() -> None:
    Tortoise.init_models(model_list, "models")


class Base(Model):
    id = fields.UUIDField(pk=True)
    created = fields.DatetimeField(auto_now_add=True)
    modified = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True
