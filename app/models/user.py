from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    email: str
    role: str = "user"

class UserResponse(BaseModel):
    user_id: int
    username: str
    email: str
    role: str
    api_key: str

    class Config:
        from_attributes = True