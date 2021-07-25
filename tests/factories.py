import factory
from factory import fuzzy

from hearty.models import IntegerTimeSeries, IntegerTimeSeriesBatch
from hearty.utils.aws.models import HttpApiRequest, RequestContext, Authorizer, Jwt
from hearty.utils.credentials import Credential


class JwtFactory(factory.Factory):
    class Meta:
        model = Jwt

    claims = factory.Dict({"sub": factory.Faker("bs"), "username": factory.Faker("bs")})


class AuthorizerFactory(factory.Factory):
    class Meta:
        model = Authorizer

    jwt = factory.SubFactory(JwtFactory)


class RequestContextFactory(factory.Factory):
    class Meta:
        model = RequestContext

    accountId = factory.Faker("bs")
    apiId = factory.Faker("bs")
    authorizer = factory.SubFactory(AuthorizerFactory)
    domainName = factory.Faker("bs")
    domainPrefix = factory.Faker("bs")
    http = factory.Dict({})
    requestId = factory.Faker("bs")
    routeKey = factory.Faker("bs")
    stage = factory.Faker("bs")
    time = factory.Faker("bs")
    timeEpoch = factory.Faker("bs")


class HttpApiRequestFactory(factory.Factory):
    class Meta:
        model = HttpApiRequest

    version = fuzzy.FuzzyChoice(["1.0", "2.0"])
    routeKey = factory.Faker("bs")
    rawPath = factory.Faker("bs")
    headers = factory.Dict({})
    requestContext = factory.SubFactory(RequestContextFactory)
    isBase64Encoded = fuzzy.FuzzyChoice([True, False])


class CredentialFactory(factory.Factory):
    class Meta:
        model = Credential

    client_id = factory.Faker("bs")
    client_secret = factory.Faker("bs")


class IntegerTimeSeriesFactory(factory.Factory):
    class Meta:
        model = IntegerTimeSeries

    start_epoch_seconds = factory.Faker("pyint")
    end_epoch_seconds = factory.Faker("pyint")
    max = factory.Faker("pyint")
    mean = factory.Faker("pydecimal")
    median = factory.Faker("pyint")
    min = factory.Faker("pyint")
    standard_deviation = factory.Faker("pydecimal")
    sample_count = factory.Faker("pyint")


class IntegerTimeSeriesBatchFactory(factory.Factory):
    class Meta:
        model = IntegerTimeSeriesBatch

    batch = factory.List([factory.SubFactory(IntegerTimeSeriesFactory) for _ in range(10)])
