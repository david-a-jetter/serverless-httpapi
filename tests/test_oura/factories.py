from datetime import datetime
import factory
from factory import fuzzy
from faker import Faker

from hearty.api.client.models import OuraAuthCodeRequest
from hearty.oura.models import (
    OuraUserAuth,
    PersonalInfo,
    Sleep,
    SleepSummary,
    Activity,
    Readiness,
    RestMode,
    ActivityResponse,
    ReadinessResponse,
    IdealBedtimeResponse,
    IdealBedtime,
    BedTimeStatus,
    BedtimeWindow,
)

fake = Faker()


class AuthCodeRequestFactory(factory.Factory):
    class Meta:
        model = OuraAuthCodeRequest

    code = factory.Faker("bs")
    redirect_uri = factory.Faker("url")


class OuraUserAuthFactory(factory.Factory):
    class Meta:
        model = OuraUserAuth

    token_type = factory.Faker("bs")
    access_token = factory.Faker("bs")
    expires_in = factory.Faker("pyint")
    refresh_token = factory.Faker("bs")


class PersonalInfoFactory(factory.Factory):
    class Meta:
        model = PersonalInfo

    age = factory.Faker("pyint")
    weight = factory.Faker("pyint")
    gender = factory.Faker("bs")
    email = factory.Faker("email")


class SleepFactory(factory.Factory):
    class Meta:
        model = Sleep

    summary_date = factory.Faker("date")
    period_id = factory.Faker("pyint")
    is_longest = factory.Faker("pyint")
    timezone = factory.Faker("pyint")
    bedtime_start = factory.LazyFunction(lambda: datetime.utcnow())
    bedtime_end = factory.LazyFunction(lambda: datetime.utcnow())
    score = factory.Faker("pyint")
    score_total = factory.Faker("pyint")
    score_disturbances = factory.Faker("pyint")
    score_efficiency = factory.Faker("pyint")
    score_latency = factory.Faker("pyint")
    score_rem = factory.Faker("pyint")
    score_deep = factory.Faker("pyint")
    score_alignment = factory.Faker("pyint")
    total = factory.Faker("pyint")
    duration = factory.Faker("pyint")
    awake = factory.Faker("pyint")
    light = factory.Faker("pyint")
    rem = factory.Faker("pyint")
    deep = factory.Faker("pyint")
    onset_latency = factory.Faker("pyint")
    restless = factory.Faker("pyint")
    efficiency = factory.Faker("pyint")
    midpoint_time = factory.Faker("pyint")
    hr_lowest = factory.Faker("pyint")
    hr_average = factory.Faker("pyfloat")
    rmssd = factory.Faker("pyint")
    breath_average = factory.Faker("pyint")
    temperature_delta = factory.Faker("pyfloat")
    hypnogram_5min = factory.LazyFunction(
        lambda: "".join([fake.lexify(text="?") for _ in range(0, 50)])
    )
    hr_5min = factory.List([_ for _ in range(0, 100)])
    rmssd_5min = factory.List([_ for _ in range(0, 100)])


class SleepSummaryFactory(factory.Factory):
    class Meta:
        model = SleepSummary

    sleep = factory.List([factory.SubFactory(SleepFactory) for _ in range(10)])


class ActivityFactory(factory.Factory):
    class Meta:
        model = Activity

    summary_date = factory.Faker("date")
    day_start = factory.LazyFunction(lambda: datetime.utcnow())
    day_end = factory.LazyFunction(lambda: datetime.utcnow())
    timezone = factory.Faker("pyint")
    score = factory.Faker("pyint")
    score_stay_active = factory.Faker("pyint")
    score_move_every_hour = factory.Faker("pyint")
    score_meet_daily_targets = factory.Faker("pyint")
    score_training_frequency = factory.Faker("pyint")
    score_training_volume = factory.Faker("pyint")
    score_recovery_time = factory.Faker("pyint")
    daily_movement = factory.Faker("pyint")
    non_wear = factory.Faker("pyint")
    rest = factory.Faker("pyint")
    inactive = factory.Faker("pyint")
    inactivity_alerts = factory.Faker("pyint")
    low = factory.Faker("pyint")
    medium = factory.Faker("pyint")
    high = factory.Faker("pyint")
    steps = factory.Faker("pyint")
    cal_total = factory.Faker("pyint")
    cal_active = factory.Faker("pyint")
    met_min_inactive = factory.Faker("pyint")
    met_min_low = factory.Faker("pyint")
    met_min_medium_plus = factory.Faker("pyint")
    met_min_medium = factory.Faker("pyint")
    met_min_high = factory.Faker("pyint")
    average_met = factory.Faker("pyfloat")
    class_5min = factory.LazyFunction(
        lambda: "".join([fake.numerify(text="?") for _ in range(0, 50)])
    )
    met_1min = factory.List([factory.Faker("pyfloat") for _ in range(0, 50)])
    rest_mode_state = fuzzy.FuzzyChoice([_ for _ in RestMode])


class ActivityResponseFactory(factory.Factory):
    class Meta:
        model = ActivityResponse

    activity = factory.List([factory.SubFactory(ActivityFactory) for _ in range(10)])


class ReadinessFactory(factory.Factory):
    class Meta:
        model = Readiness

    summary_date = factory.Faker("date")
    period_id = factory.Faker("pyint")
    score = factory.Faker("pyint")
    score_previous_night = factory.Faker("pyint")
    score_sleep_balance = factory.Faker("pyint")
    score_previous_day = factory.Faker("pyint")
    score_activity_balance = factory.Faker("pyint")
    score_resting_hr = factory.Faker("pyint")
    score_hrv_balance = factory.Faker("pyint")
    score_recovery_index = factory.Faker("pyint")
    score_temperature = factory.Faker("pyint")
    rest_mode_state = factory.Faker("pyint")


class ReadinessResponseFactory(factory.Factory):
    class Meta:
        model = ReadinessResponse

    readiness = factory.List([factory.SubFactory(ReadinessFactory) for _ in range(10)])


class BedtimeWindowFactory(factory.Factory):
    class Meta:
        model = BedtimeWindow

    start = factory.Faker("pyint")
    end = factory.Faker("pyint")


class IdealBedtimeFactory(factory.Factory):
    class Meta:
        model = IdealBedtime

    date = factory.Faker("date")
    bedtime_window = factory.SubFactory(BedtimeWindowFactory)
    status = fuzzy.FuzzyChoice([_ for _ in BedTimeStatus])


class IdealBedtimeResponseFactory(factory.Factory):
    class Meta:
        model = IdealBedtimeResponse

    ideal_bedtimes = factory.List([factory.SubFactory(IdealBedtimeFactory) for _ in range(10)])
