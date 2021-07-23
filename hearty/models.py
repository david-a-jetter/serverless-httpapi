from typing import Optional

from pydantic import BaseModel, EmailStr


class Patient(BaseModel):
    id: str
    email: EmailStr


class TimeSeriesData(BaseModel):
    start_epoch_seconds: int
    end_epoch_seconds: int
    max: Optional[float]
    mean: Optional[float]
    median: Optional[float]
    min: Optional[float]
    standard_deviation: Optional[float]
    sample_count: Optional[int]
