from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt

from config.secrets import JWT
from config.exceptions import UNAUTHORIZED
from models.user import User, UserPydantic

router = APIRouter(
    prefix='/token',
    tags=['token']
)

oauth2_scheme = OAuth2PasswordBearer('/token')


@ router.post('/')
async def generate_token(
        form_data: OAuth2PasswordRequestForm = Depends()):
    user = await User.authenticate_user(
        form_data.username,
        form_data.password)
    user_pydantic = await UserPydantic.from_tortoise_orm(user)
    user_dict = user_pydantic.dict(
        include={'id', 'name', 'username'})
    user_dict['id'] = str(user_dict['id'])
    token = jwt.encode(user_dict,
                       key=JWT.key, algorithm=JWT.algorithm)
    return {"access_token": token, "token_type": "bearer"}


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, key=JWT.key, algorithms=[JWT.algorithm])
        user = await User.get(pk=payload.get('id'))
        if not user:
            raise UNAUTHORIZED
        return user
    except:
        raise UNAUTHORIZED
