from pydantic import BaseModel, EmailStr


class ApiResponse(BaseModel):
    message: str


class ApiError(BaseModel):
    error: str


class Patient(BaseModel):
    id: str
    email: EmailStr
