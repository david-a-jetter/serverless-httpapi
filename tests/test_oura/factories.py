import factory

from hearty.oura.models import AuthCodeRequest


class AuthCodeRequestFactory(factory.Factory):
    class Meta:
        model = AuthCodeRequest

    code = factory.Faker("bs")
    redirect_uri = factory.Faker("url")
