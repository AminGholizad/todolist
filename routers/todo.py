from uuid import UUID
from fastapi import APIRouter, Depends

from models.todo import Todo, TodoPutPydantic, TodoPydantic, TodoPostPydantic
from models.user import User
from routers.token import get_current_user

router = APIRouter(
    prefix='/my/todolist',
    tags=['todolist']
)


@ router.get('/')
async def get_todolist(user: User = Depends(get_current_user)):
    return await TodoPydantic.from_queryset(user.todolist.all())


@ router.post('/')
async def add_todo(todo: TodoPostPydantic,
                   user: User = Depends(get_current_user)):
    todo_obj = await Todo.create(**todo.dict(), user=user)
    return await TodoPydantic.from_tortoise_orm(todo_obj)


@ router.get('/{todo_id}')
async def get_todo(todo_id: UUID,
                   user: User = Depends(get_current_user)):
    return await TodoPydantic.from_queryset_single(user.todolist.filter(pk=todo_id).first())


@ router.put('/{todo_id}')
async def edit_todo(todo: TodoPutPydantic,
                    todo_id: UUID,
                    user: User = Depends(get_current_user)):
    todo_obj = await user.todolist.filter(pk=todo_id).first()
    todo_obj.update_from_dict(todo.dict(exclude_unset=True))
    await todo_obj.save()
    return await TodoPydantic.from_tortoise_orm(todo_obj)


@ router.delete('/{todo_id}')
async def delete_todo(todo_id: UUID,
                      user: User = Depends(get_current_user)):
    await user.todolist.filter(pk=todo_id).delete()
    return {}
