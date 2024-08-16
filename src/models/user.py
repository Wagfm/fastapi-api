from dataclasses import dataclass
from uuid import UUID

from models.base import BaseModel


@dataclass(frozen=True)
class User(BaseModel):
    id: UUID
    email: str
    name: str
    searchable: str
