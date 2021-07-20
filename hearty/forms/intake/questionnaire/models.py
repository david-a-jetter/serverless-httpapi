from datetime import date
from enum import IntEnum, Enum
from typing import Optional, List

from pydantic import BaseModel, EmailStr


class Address(BaseModel):
    line_one: str
    line_two: Optional[str]
    city: str
    state: str
    postal_code: str


class Race(IntEnum):
    BALANCE = 0
    AMERICAN_INDIAN_ALASKA_NATIVE = 1
    ASIAN = 2
    BLACK_AFRICAN_AMERICAN = 3
    NATIVE_HAWAIIAN_PACIFIC_ISLANDER = 4
    WHITE = 5


class Ethnicity(IntEnum):
    HISPANIC_LATINO = 0
    NOT_HISPANIC = 1


class GeneticBackground(IntEnum):
    OTHER = 0
    AFRICAN_AMERICAN = 1
    HISPANIC = 2
    MEDITERRANEAN = 3
    ASIAN = 4
    NATIVE_AMERICAN = 5
    CAUCASIAN = 6
    NORTHERN_EUROPEAN = 7


class PhoneContactInfo(BaseModel):
    home_phone: Optional[str]
    cell_phone: Optional[str]
    work_phone: Optional[str]


class ReferralSource(IntEnum):
    OTHER = 0
    CLINIC_WEBSITE = 1
    IFM_WEBSITE = 2
    DOCTOR_REFERRAL = 3
    FRIEND_FAMILY_REFERRAL = 4
    SOCIAL_MEDIA = 5


class GeneralInfo(BaseModel):
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: str
    date_of_birth: date
    email: Optional[EmailStr]
    contact_info: Optional[PhoneContactInfo]
    genetic_background: List[GeneticBackground]
    genetic_background_other: Optional[str]
    last_medical_care: Optional[str]
    emergency_contact_name: Optional[str]
    emergency_contact_relationship: Optional[str]
    emergency_contact_phone: PhoneContactInfo
    referral_source: ReferralSource
    referral_other: Optional[str]


class Severity(Enum):
    MILD = "Mild"
    MODERATE = "Moderate"
    SEVERE = "Severe"


class TreatmentSuccess(Enum):
    EXCELLENT = "Excellent"
    GOOD = "Good"
    FAIR = "Fair"


class HealthConcern(BaseModel):
    description: str
    severity: Severity
    treatment: Optional[str]
    treatment_success: Optional[TreatmentSuccess]


class Allergy(BaseModel):
    substance: str
    reaction: str


class Sleep(BaseModel):
    average_hours: int
    problem_falling_asleep: bool
    problem_staying_asleep: bool
    insomnia: bool
    snore: bool
    feel_rested: bool
    sleeping_aids: bool
    sleeping_aid_description: Optional[str]


class ActivityType(IntEnum):
    OTHER = 0
    CARDIO_AEROBIC = 1
    STRENGTH_RESISTANCE = 2
    FLEXIBILITY_STRETCHING = 3
    BALANCE = 4
    SPORTS_LEISURE = 5


class ExerciseActivity(BaseModel):
    activity_type: ActivityType
    description: str
    times_per_week: int
    minutes_per_session: int


class Motivation(IntEnum):
    NO = 0
    LITTLE = 1
    YES = 2


class Exercise(BaseModel):
    exercise: List[ExerciseActivity]
    motivation: Motivation
    limitations: bool
    limitations_description: Optional[str]
    fatigue_afterwards: bool
    fatigue_description: Optional[str]


class Lifestyle(BaseModel):
    sleep: Sleep
    exercise: Exercise


class IntakeForm(BaseModel):
    general_info: GeneralInfo
    current_concerns: List[HealthConcern]
    allergies: List[Allergy]
    lifestyle: Lifestyle
