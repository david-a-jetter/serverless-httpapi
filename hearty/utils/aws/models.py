from http import HTTPStatus
from typing import List, Dict, Optional
from pydantic import BaseModel


class Jwt(BaseModel):
    # https://openid.net/specs/openid-connect-core-1_0.html#StandardClaims
    claims: Dict[str, str]
    scopes: Optional[Dict[str, str]]

    @property
    def sub(self) -> str:
        return self.claims["sub"]

    @property
    def username(self) -> str:
        return self.claims["username"]


class Authorizer(BaseModel):
    jwt: Jwt


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
    queryStringParameters: Dict[str, str] = {}
    requestContext: RequestContext
    pathParameters: Dict[str, str] = {}
    isBase64Encoded: bool

    @property
    def jwt(self) -> Jwt:
        authorizer = self.requestContext.authorizer
        if authorizer is None:
            raise ValueError("No authorizer on this request")
        return authorizer.jwt


class HttpApiPostRequest(HttpApiRequest):
    body: str


class HttpApiResponse(BaseModel):
    cookies: Optional[List[str]]
    isBase64Encoded: bool = False
    statusCode: int = HTTPStatus.OK.value
    headers: Dict[str, str] = {"content-type": "application/json"}
    body: Optional[str]
