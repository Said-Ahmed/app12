from typing import List

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends

from src.auth.dependencies import get_current_user
from src.auth.models import Users
from src.posts.dao import PostsDAO
from src.posts.exceptions import PostNotFoundException
from src.posts.schemas import SPostCreate, SProductResponse

router = APIRouter(
    prefix='/posts',
    tags=['Posts $ Посты'],
)


@router.get(
    "",
    response_model=List[SProductResponse]
)
async def get_posts(current_user: Users = Depends(get_current_user)):
    return await PostsDAO.find_all()


@router.post(
    "/add",
    status_code=201,
    response_model=SProductResponse
)
async def add_post(
        post: SPostCreate,
        current_user: Users = Depends(get_current_user)
):
    post = await PostsDAO.add(**post.model_dump(), user_id=current_user.id)
    return post


@router.delete("/delete/{post_id}")
async def delete_post(
        post_id: int,
        current_user: Users = Depends(get_current_user)
):
    post = await PostsDAO.find_by_id(post_id)
    if not post:
        raise PostNotFoundException

    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="У вас нет прав"
        )

    await PostsDAO.delete(post_id)

