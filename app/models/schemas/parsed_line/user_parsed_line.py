from pydantic import BaseModel


class UserParsedLine(BaseModel):
    user_id: int
    name: str
