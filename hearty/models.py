from decimal import Decimal
from typing import Optional, List

from pydantic import BaseModel, EmailStr


TIME_SERIES_START = "start_epoch_seconds"


class Patient(BaseModel):
    id: str
    email: EmailStr


class BaseTimeSeries(BaseModel):
    start_epoch_seconds: int
    end_epoch_seconds: int
    mean: Optional[Decimal]
    standard_deviation: Optional[Decimal]
    sample_count: Optional[int]


class IntegerTimeSeries(BaseTimeSeries):
    max: Optional[int]
    median: Optional[int]
    min: Optional[int]


class IntegerTimeSeriesBatch(BaseModel):
    batch: List[IntegerTimeSeries]


class DecimalTimeSeries(BaseTimeSeries):
    max: Optional[Decimal]
    median: Optional[Decimal]
    min: Optional[Decimal]


class DecimalTimeSeriesBatch(BaseModel):
    batch: List[DecimalTimeSeries]
