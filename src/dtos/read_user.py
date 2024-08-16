from uuid import UUID

from dtos.base import BaseDto


class ReadUserDto(BaseDto):
    id: UUID
    name: str
    email: str
