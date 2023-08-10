from typing import Optional
from uuid import UUID

from fastapi import UploadFile

from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class BaseModelDict(BaseModel):
    model_config = ConfigDict(
        from_attributes=True, protected_namespaces=("_protected",)
    )

    def dict(self, *args, **kwargs) -> dict[str, Any]:
        values = super().model_dump(*args, **kwargs)
        for k, v in values.items():
            if isinstance(v, (datetime, date)):
                values[k] = v.isoformat()

        return values


class ProductDelete(BaseModelDict):
    uuid: UUID
    permanent: bool = False


class ProductUpdate(BaseModelDict):
    uuid: UUID | str
    name: Optional[str]
    file: Optional[str | UploadFile]


class ProductRetrieve(BaseModelDict):
    uuid: UUID | str
    name: str
    file: str


class ProductCreate(BaseModelDict):
    name: str
    file: Optional[str]
