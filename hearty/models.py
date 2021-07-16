from pydantic import BaseModel, EmailStr


class Patient(BaseModel):
    id: str
    email: EmailStr
