from typing import Optional, List

from pydantic import BaseModel, EmailStr


TIME_SERIES_START = "start_epoch_seconds"


class Patient(BaseModel):
    id: str
    email: EmailStr


class BaseTimeSeries(BaseModel):
    start_epoch_seconds: int
    end_epoch_seconds: int
    mean: Optional[float]
    standard_deviation: Optional[float]
    sample_count: Optional[int]


class IntegerTimeSeries(BaseTimeSeries):
    max: Optional[int]
    median: Optional[int]
    min: Optional[int]


class IntegerTimeSeriesBatch(BaseModel):
    batch: List[IntegerTimeSeries]


class FloatTimeSeries(BaseTimeSeries):
    max: Optional[float]
    median: Optional[float]
    min: Optional[float]


class FloatTimeSeriesBatch(BaseModel):
    batch: List[FloatTimeSeries]
