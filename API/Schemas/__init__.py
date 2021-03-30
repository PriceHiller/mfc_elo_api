from typing import Optional
from typing import Union
from typing import List

from datetime import datetime
from datetime import timezone

from pydantic import UUID4
from pydantic import Field
from pydantic import validator
from pydantic import BaseModel


class BaseSchema(BaseModel):
    generated: datetime = None
    message: str = None
    extra: List[dict] = None

    @validator("generated", pre=True, always=True)
    def set_generated_datetime_now(cls, v):
        return v or datetime.now(tz=timezone.utc)


class BaseInDB(BaseSchema):
    id: Optional[Union[UUID4, str, int]] = Field(..., minlength=32, maxlength=36)
    creation: Optional[datetime]
    modification: Optional[datetime]
