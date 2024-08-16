from pydantic import field_validator

from dtos.base import BaseDto


class CreateUserDto(BaseDto):
    name: str
    email: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, name: str) -> str:
        if len(name) == 0 or len(name) > 50:
            raise ValueError("name must be less than 50 characters and not empty")
        return name

    @field_validator("email")
    @classmethod
    def validate_email(cls, email: str) -> str:
        if len(email) == 0 or len(email) > 50:
            raise ValueError("email must be less than 50 characters and not empty")
        return email
