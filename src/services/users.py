from typing import Optional
from uuid import UUID

from dtos.create_user import CreateUserDto
from dtos.read_user import ReadUserDto
from models.user import User
from repositories.base import BaseRepository
from repositories.users import UsersRepository


class UsersService:
    def __init__(self):
        self._repository: BaseRepository[User] = UsersRepository()

    def create(self, dto: CreateUserDto) -> ReadUserDto:
        user_model = self._repository.create(dto)
        return ReadUserDto(**user_model.to_dict())

    def read_by_id(self, id: UUID) -> Optional[ReadUserDto]:
        user_model = self._repository.read_by_id(id)
        if user_model is None:
            return None
        return ReadUserDto(**user_model.to_dict())
