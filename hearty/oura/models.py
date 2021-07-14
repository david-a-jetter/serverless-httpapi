from datetime import date, datetime
from enum import IntEnum, Enum
from typing import Optional, List
from pydantic import BaseModel, Field


class AuthCodeRequest(BaseModel):
    code: str
    redirect_uri: Optional[str]


class OuraUserAuth(BaseModel):
    token_type: str
    access_token: str
    expires_in: int
    refresh_token: str


class PersonalInfo(BaseModel):
    # https://cloud.ouraring.com/docs/personal-info
    age: int
    weight: int
    gender: str
    email: str


class Readiness(BaseModel):
    # https://cloud.ouraring.com/docs/readiness
    summary_date: date
    period_id: int
    score: int
    score_previous_night: int
    score_sleep_balance: int
    score_previous_day: int
    score_activity_balance: int
    score_resting_hr: int
    score_hrv_balance: int
    score_recovery_index: int
    score_temperature: int
    rest_mode_state: int


class ReadinessResponse(BaseModel):
    readiness: List[Readiness]


class Sleep(BaseModel):
    # https://cloud.ouraring.com/docs/sleep
    summary_date: date
    period_id: int
    is_longest: int
    timezone: int
    bedtime_start: datetime
    bedtime_end: datetime
    score: int
    score_total: int
    score_disturbances: int
    score_efficiency: int
    score_latency: int
    score_rem: int
    score_deep: int
    score_alignment: int
    total: int
    duration: int
    awake: int
    light: int
    rem: int
    deep: int
    onset_latency: int
    restless: int
    efficiency: int
    midpoint_time: int
    hr_lowest: int
    hr_average: float
    rmssd: int
    breath_average: int
    temperature_delta: float
    hypnogram_5min: str
    hr_5min: List[int]
    rmssd_5min: List[int]


class SleepSummary(BaseModel):
    sleep: List[Sleep]


class ActivityClass(IntEnum):
    NON_WEAR = 0
    REST = 1
    INACTIVE = 2
    LOW = 3
    MEDIUM = 4
    HIGH = 5


class RestMode(IntEnum):
    OFF = 0
    ENTERING_REST_MODE = 1
    REST_MODE = 2
    ENTERING_RECOVERY = 3
    RECOVERING = 4


class Activity(BaseModel):
    # https://cloud.ouraring.com/docs/activity
    summary_date: date
    day_start: datetime
    day_end: datetime
    timezone: int
    score: int
    score_stay_active: int
    score_move_every_hour: int
    score_meet_daily_targets: int
    score_training_frequency: int
    score_training_volume: int
    score_recovery_time: int
    daily_movement: int
    non_wear: int
    rest: int
    inactive: int
    inactivity_alerts: int
    low: int
    medium: int
    high: int
    steps: int
    cal_total: int
    cal_active: int
    met_min_inactive: int
    met_min_low: int
    met_min_medium_plus: int
    met_min_medium: int
    met_min_high: int
    average_met: float
    class_5min: str = Field(
        ...,
        description="A string that contains one character for each starting five minutes "
        "of the activity period, so that the first period starts from 4 AM "
        "local time. Enum of range of values is ActivityClass",
    )
    met_1min: List[float] = Field(
        ...,
        description="Average MET level for each minute of the activity period, "
        "starting from 4 AM local time.",
    )
    rest_mode_state: RestMode


class ActivityResponse(BaseModel):
    activity: List[Activity]


class BedtimeWindow(BaseModel):
    start: int
    end: int


class BedTimeStatus(Enum):
    NOT_ENOUGH_DATA = "NOT_ENOUGH_DATA"
    LOW_SLEEP_SCORES = "LOW_SLEEP_SCORES"
    IDEAL_BEDTIME_AVAILABLE = "IDEAL_BEDTIME_AVAILABLE"


class IdealBedtime(BaseModel):
    class Config:
        allow_population_by_field_name = True

    # https://cloud.ouraring.com/docs/bedtime
    summary_date: date = Field(..., alias="date")
    bedtime_window: BedtimeWindow
    status: BedTimeStatus


class IdealBedtimeResponse(BaseModel):
    ideal_bedtimes: List[IdealBedtime]
