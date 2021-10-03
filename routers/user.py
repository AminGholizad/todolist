from fastapi import APIRouter
from fastapi.params import Depends
from passlib.hash import bcrypt_sha256

from models.user import User, UserPutPydantic, UserPostPydantic, UserPydantic
from routers.token import get_current_user

router = APIRouter(
    prefix='/user',
    tags=['user']
)


@ router.post('/')
async def add_user(user: UserPostPydantic):
    user_obj = await User.create(**user.dict(exclude={'password'}), password=bcrypt_sha256.hash(user.password))
    return await UserPydantic.from_tortoise_orm(user_obj)


@ router.get('/')
async def get_user(user: User = Depends(get_current_user)):
    await user.refresh_from_db()
    return await UserPydantic.from_tortoise_orm(user)


@ router.put('/')
async def edit_user(user_in: UserPutPydantic, user: User = Depends(get_current_user)):
    user_dict = user_in.dict(exclude_unset=True)
    if 'password' in user_dict.keys():
        user_dict['password'] = bcrypt_sha256.hash(user_dict['password'])
    user.update_from_dict(user_dict)
    await user.save()
    return await UserPydantic.from_tortoise_orm(user)


@ router.delete('/')
async def delete_user(user: User = Depends(get_current_user)):
    await user.delete()
    return {}
