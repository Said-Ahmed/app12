from src.dao.base import BaseDAO
from src.auth.models import Users


class UsersDAO(BaseDAO):
    model = Users