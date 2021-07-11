import logging
from typing import Optional, Dict
from requests import Session, HTTPError

from hearty.oura.constants import OURA_APP_NAME
from hearty.oura.models import OuraUserAuth, OuraResources, PersonalInfo
from hearty.utils.credentials import build_credentials_repo
from hearty.utils.requests import mount_logging_adapters

_API_HOST = "https://api.ouraring.com/"
logger = logging.getLogger(__name__)


class OuraUserAuthorizer:
    @classmethod
    def build(cls, environment: str):

        secrets_repo = build_credentials_repo(environment)
        secret = secrets_repo.get_item(OURA_APP_NAME)
        if secret is None:
            raise ValueError(
                f"No credentials for app {OURA_APP_NAME} found for environment {environment}"
            )
        if not secret.client_id or not secret.client_secret:
            raise ValueError("Client Id and Client Secret are both mandatory")
        session = Session()
        mount_logging_adapters(session)
        session.auth = (secret.client_id, secret.client_secret)
        return cls(session)

    def __init__(self, session: Session):
        self._session = session

    def authorize_user(self, auth_code: str, redirect_uri: Optional[str]) -> OuraUserAuth:

        payload = {"grant_type": "authorization_code", "code": auth_code}
        if redirect_uri:
            payload["redirect_uri"] = redirect_uri

        return self._get_access_token(payload)

    def refresh_user(self, refresh_token) -> OuraUserAuth:
        payload = {"grant_type": "refresh_token", "refresh_token": refresh_token}
        return self._get_access_token(payload)

    def _get_access_token(self, payload: Dict[str, str]) -> OuraUserAuth:
        url = _API_HOST + OuraResources.AccessToken.value
        response = self._session.post(url, data=payload)

        if response.ok:
            return OuraUserAuth.parse_raw(response.text)
        else:
            raise HTTPError(f"{response.status_code}: {response.text}")


class OuraApiAccess:
    @classmethod
    def build(cls, access_token: str):
        session = Session()
        session.headers["Authorization"] = f"Bearer {access_token}"
        mount_logging_adapters(session)
        return cls(session)

    def __init__(self, session: Session):
        self._session = session

    def get_personal_info(self) -> PersonalInfo:

        url = _API_HOST + OuraResources.PersonalInfo.value
        response = self._session.get(url)

        if response.ok:
            return PersonalInfo.parse_raw(response.text)
        else:
            raise HTTPError(f"{response.status_code}: {response.text}")
