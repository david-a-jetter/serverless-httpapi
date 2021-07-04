from typing import List, Dict, Optional
from pydantic import BaseModel


class Jwt(BaseModel):
    # https://openid.net/specs/openid-connect-core-1_0.html#StandardClaims
    claims: Optional[Dict[str, str]]
    scopes: Optional[Dict[str, str]]

    @property
    def sub(self) -> Optional[str]:
        if self.claims:
            return self.claims.get("sub")
        else:
            return None

    @property
    def username(self) -> Optional[str]:
        if self.claims:
            return self.claims.get("username")
        else:
            return None


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


class ApiRequest(BaseModel):
    # https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html
    version: str
    routeKey: str
    rawPath: str
    rawQueryString: Optional[str]
    cookies: Optional[List[str]]
    headers: Dict[str, str]
    queryStringParameters: Optional[Dict[str, str]]
    requestContext: RequestContext
    body: Optional[str]
    isBase64Encoded: Optional[bool]
