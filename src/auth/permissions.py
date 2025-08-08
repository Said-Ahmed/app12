from typing import List
from fastapi import Request
from fastapi.params import Depends
from starlette import status
from starlette.exceptions import HTTPException

from src.auth.dependencies import get_current_user
from src.auth.schemas import SUserRegister


class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: SUserRegister = Depends(get_current_user), request: Request=None):
        if current_user.is_admin:
            return True
        user_id = request.path_params.get("user_id")

        if 'owner' in self.allowed_roles and user_id and str(current_user.id) == user_id:
            return True

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="У вас нет прав"
        )
