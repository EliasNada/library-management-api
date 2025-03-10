from pydantic import BaseModel


class RegisterResponse(BaseModel):
    access_token: str
    token_type: str
    api_key: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str


class NewApiKey(BaseModel):
    api_key: str
