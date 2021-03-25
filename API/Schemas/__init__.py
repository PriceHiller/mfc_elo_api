from typing import Optional, Union
from datetime import datetime

from pydantic import UUID4, Field

from pydantic import BaseModel


class BaseInDB(BaseModel):
    id: Optional[Union[UUID4, str, int]] = Field(..., minlength=32, maxlength=36)
    creation: Optional[datetime]
    modification: Optional[datetime]
