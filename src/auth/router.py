from fastapi import APIRouter, Response
from fastapi.params import Depends

from src.auth.permissions import RoleChecker
from src.auth.schemas import SUserUpdate, SUserDetail
from src.auth.auth import get_password_hash, authenticate_user, create_access_token
from src.auth.dao import UsersDAO
from src.auth.dependencies import get_current_user
from src.auth.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException, UserNotFoundException
from src.auth.models import Users
from src.auth.schemas import SUserAuth, SUserRegister

router = APIRouter(
    prefix='/auth',
    tags=['Auth $ Пользователи'],
)


@router.post('/register')
async def register_user(user_data: SUserRegister):
    user = await UsersDAO.find_one_or_none(email=user_data.email)

    if user:
        raise UserAlreadyExistsException

    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(
        email=user_data.email,
        hashed_password=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        middle_name=user_data.middle_name,
        is_admin=user_data.is_admin
    )


@router.post('/login')
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)

    if not user or not user.is_active:
        raise IncorrectEmailOrPasswordException

    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie('access_token', access_token, httponly=True)

    return {'access_token': access_token, 'is_admin': user.is_admin}


@router.post('/logout')
async def logout_user(response: Response):
    response.delete_cookie('access_token')


@router.delete(
    '/delete/{user_id}',
    dependencies=[Depends(RoleChecker(['admin', 'owner']))]
)
async def delete_user(
        user_id: int,
        response: Response
):
    user = await UsersDAO.find_one_or_none(id=user_id)
    if not user:
        raise UserNotFoundException

    user = await UsersDAO.update(id=user_id, is_active=False)
    response.delete_cookie('access_token')


@router.patch(
    '/update/{user_id}',
    dependencies=[Depends(RoleChecker(['admin', 'owner']))]
)
async def update_user(
        user_id: int,
        update_data: SUserUpdate
) -> SUserDetail:
    user = await UsersDAO.find_one_or_none(id=user_id)
    if not user:
        raise UserNotFoundException

    user = await UsersDAO.update(id=user_id, **update_data.model_dump(exclude_unset=True))
    return user


@router.get('/me')
async def get_current_user(current_user: Users = Depends(get_current_user)):
    return current_user


