from pydantic import BaseModel


class ExtraModel(BaseModel):
    class Config:
        extra = "allow"
