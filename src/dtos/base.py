from typing import Any

from pydantic import BaseModel


class BaseDto(BaseModel):
    def get_fields_values(self, exclude_none: bool = False) -> tuple[list[str], list[Any]]:
        data = self.model_dump(exclude_none=exclude_none)
        fields = [field for field in data]
        values = [data[field] for field in fields]
        return fields, values
