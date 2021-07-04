from typing import Optional
from pydantic import BaseModel


class AuthCodeRequest(BaseModel):
    code: str
    redirect_uri: Optional[str]
