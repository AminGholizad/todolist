from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from models.base import model_list
from config.secrets import db_url


def register(app: FastAPI):
    register_tortoise(
        app, db_url=db_url,
        modules={'models': model_list},
        generate_schemas=True,
        add_exception_handlers=True
    )
