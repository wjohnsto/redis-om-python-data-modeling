from redis_om import (Field, HashModel)


class User(HashModel):
    name: str = Field(index=True)
