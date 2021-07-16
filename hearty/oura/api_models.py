from typing import Optional

from pydantic import BaseModel


class OuraAuthCodeRequest(BaseModel):
    code: str
    redirect_uri: Optional[str]
