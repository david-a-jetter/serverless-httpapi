import factory
from factory import fuzzy
from hearty.utils.aws.models import HttpApiRequest, RequestContext, Authorizer, Jwt


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
    http = {}
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
    headers = {}
    requestContext = factory.SubFactory(RequestContextFactory)
    isBase64Encoded = fuzzy.FuzzyChoice([True, False])
