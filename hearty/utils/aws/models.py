from typing import List, Dict, Optional
from pydantic import BaseModel


class Jwt(BaseModel):
    # https://openid.net/specs/openid-connect-core-1_0.html#StandardClaims
    claims: Dict[str, str] = {}
    scopes: Dict[str, str] = {}

    @property
    def sub(self) -> str:
        return self.claims["sub"]

    @property
    def username(self) -> str:
        return self.claims["username"]


class Authorizer(BaseModel):
    jwt: Optional[Jwt]


class RequestContext(BaseModel):
    accountId: str
    apiId: str
    # authentication: Ignore this for now
    authorizer: Optional[Authorizer]
    domainName: str
    domainPrefix: str
    http: Dict[str, str]
    requestId: str
    routeKey: str
    stage: str
    time: str
    timeEpoch: str


class HttpApiRequest(BaseModel):
    # https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html
    version: str
    routeKey: str
    rawPath: str
    rawQueryString: Optional[str]
    cookies: Optional[List[str]]
    headers: Dict[str, str]
    queryStringParameters: Optional[Dict[str, str]]
    requestContext: RequestContext
    body: str = ""
    isBase64Encoded: bool

    @property
    def jwt(self) -> Jwt:
        authorizer = self.requestContext.authorizer
        if authorizer is None:
            raise ValueError("No authorizer on this request")
        jwt = authorizer.jwt
        if jwt is None:
            raise ValueError("jwt not used for this authorizer")
        else:
            return jwt


class HttpApiResponse(BaseModel):
    cookies: Optional[List[str]]
    isBase64Encoded: bool = False
    statusCode: int = 200
    headers: Optional[Dict[str, str]] = {"content-type": "application/json"}
    body: Optional[str]
