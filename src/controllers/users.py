from uuid import UUID

import psycopg
from fastapi import Response

from dtos.create_user import CreateUserDto
from services.users import UsersService


class UsersController:
    def __init__(self):
        self._service = UsersService()

    async def create(self, dto: CreateUserDto, response: Response) -> dict:
        try:
            created_user = self._service.create(dto)
            response.headers["Location"] = f"/users/{created_user.id}"
            return created_user.model_dump()
        except psycopg.IntegrityError:
            response.status_code = 400
            return {"message": "user already exists"}
        except psycopg.Error:
            response.status_code = 422
            return {"message": "user could not be created"}
        except Exception as exception:
            response.status_code = 500
            return {"message": f"{exception}"}

    async def read_by_id(self, id: UUID, response: Response) -> dict:
        try:
            dto = self._service.read_by_id(id)
            if dto is None:
                response.status_code = 404
                return {"message": "user not found"}
            return dto.model_dump()
        except Exception as exception:
            response.status_code = 500
            return {"message": f"{exception}"}
