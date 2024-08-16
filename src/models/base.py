import dataclasses
from dataclasses import dataclass, fields


@dataclass(frozen=True)
class BaseModel:
    @classmethod
    def from_dict(cls, data: dict) -> "BaseModel":
        model_fields = [field.name for field in fields(cls)]
        valid_data = {field: value for field, value in data.items() if field in model_fields}
        return cls(**valid_data)

    def to_dict(self, exclude_none: bool = False) -> dict:
        data = dataclasses.asdict(self)
        if not exclude_none:
            return data
        return {key: value for key, value in data if value is not None}
