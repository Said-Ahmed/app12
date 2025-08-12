from fastapi import HTTPException, status

PostNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Пост не найден'
)