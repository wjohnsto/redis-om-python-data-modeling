from pydantic import validator
from redis_om import (Field, JsonModel, EmbeddedJsonModel)
from typing import List, Optional


class TaskAssignee(EmbeddedJsonModel):
    user_id: str = Field(index=True)


class Task(JsonModel):
    name: str = Field(index=True)
    status: str = Field(index=True)
    description: Optional[str] = Field(index=True, full_text_search=True)
    assigned_to: Optional[List[TaskAssignee]] = []

    @validator('status')
    def status_must_be_in_list(cls, v):
        if v.lower() not in ['new', 'in progress', 'done']:
            raise ValueError(
                f'{v} is not a valid status, must be in [new, in progress, done]')
        return v.upper()
