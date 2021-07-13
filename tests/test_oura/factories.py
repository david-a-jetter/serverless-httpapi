import factory
from factory import fuzzy

from hearty.oura.models import AuthCodeRequest, OuraUserAuth, PersonalInfo


class AuthCodeRequestFactory(factory.Factory):
    class Meta:
        model = AuthCodeRequest

    code = factory.Faker("bs")
    redirect_uri = factory.Faker("url")


class OuraUserAuthFactory(factory.Factory):
    class Meta:
        model = OuraUserAuth

    token_type = factory.Faker("bs")
    access_token = factory.Faker("bs")
    expires_in = fuzzy.FuzzyInteger(low=0, high=10000)
    refresh_token = factory.Faker("bs")


class PersonalInfoFactory(factory.Factory):
    class Meta:
        model = PersonalInfo

    age = fuzzy.FuzzyInteger(low=0, high=10000)
    weight = fuzzy.FuzzyInteger(low=0, high=10000)
    gender = factory.Faker("bs")
    email = factory.Faker("email")
