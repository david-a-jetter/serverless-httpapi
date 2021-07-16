import logging
from datetime import date
from enum import Enum
from typing import Dict, Type

from pydantic import BaseModel
from requests import Session, HTTPError

from hearty.oura.constants import OURA_APP_NAME
from hearty.oura.api_models import OuraAuthCodeRequest
from hearty.oura.models import (
    OuraUserAuth,
    PersonalInfo,
    SleepSummary,
    ActivityResponse,
    ReadinessResponse,
    IdealBedtimeResponse,
)
from hearty.utils.credentials import build_credentials_repo
from hearty.utils.requests import mount_logging_adapters

_API_HOST = "https://api.ouraring.com/"
logger = logging.getLogger(__name__)


class OuraResources(Enum):
    AccessToken = "oauth/token"
    PersonalInfo = "v1/userinfo"
    Sleep = "v1/sleep"
    Activity = "v1/activity"
    Readiness = "v1/readiness"
    Bedtime = "v1/bedtime"


class OuraUserAuthorizer:
    @classmethod
    def build(cls, environment: str):

        cred_repo = build_credentials_repo(environment)
        credential = cred_repo.get_item(OURA_APP_NAME)
        if credential is None:
            raise ValueError(
                f"No credentials for app {OURA_APP_NAME} found for environment {environment}"
            )
        if not credential.client_id or not credential.client_secret:
            raise ValueError("Client Id and Client Secret are both mandatory")
        session = Session()
        mount_logging_adapters(session)
        session.auth = (credential.client_id, credential.client_secret)
        return cls(session)

    def __init__(self, session: Session):
        self._session = session

    def authorize_user(self, auth_request: OuraAuthCodeRequest) -> OuraUserAuth:

        payload = {"grant_type": "authorization_code", "code": auth_request.code}
        if auth_request.redirect_uri:
            payload["redirect_uri"] = auth_request.redirect_uri

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

    def get_sleep_summaries(self, start: date, end: date) -> SleepSummary:
        url = _API_HOST + OuraResources.Sleep.value
        params = {"start": str(start), "end": str(end)}

        return self._make_get_call(url, SleepSummary, params)  # type: ignore[return-value]

    def get_activity_summaries(self, start: date, end: date) -> ActivityResponse:
        url = _API_HOST + OuraResources.Activity.value
        params = {"start": str(start), "end": str(end)}

        return self._make_get_call(url, ActivityResponse, params)  # type: ignore[return-value]

    def get_readiness_summaries(self, start: date, end: date) -> ReadinessResponse:
        url = _API_HOST + OuraResources.Readiness.value
        params = {"start": str(start), "end": str(end)}

        return self._make_get_call(url, ReadinessResponse, params)  # type: ignore[return-value]

    def get_ideal_bedtimes(self, start: date, end: date) -> IdealBedtimeResponse:
        url = _API_HOST + OuraResources.Bedtime.value
        params = {"start": str(start), "end": str(end)}

        return self._make_get_call(url, IdealBedtimeResponse, params)  # type: ignore[return-value]

    def _make_get_call(
        self, url: str, response_model: Type[BaseModel], params: Dict[str, str]
    ) -> BaseModel:

        response = self._session.get(url, params=params)

        if response.ok:
            return response_model.parse_raw(response.text)
        else:
            raise HTTPError(f"{response.status_code}: {response.text}")
