from pydantic import BaseModel


class ApiResponse(BaseModel):
    message: str


class ApiError(BaseModel):
    error: str
