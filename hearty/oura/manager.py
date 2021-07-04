from __future__ import annotations

from typing import Optional
from hearty.models import Patient
from hearty.oura.api import OuraApiAccess, OuraUserAuthorizer, PersonalInfo, OuraUserAuth
from hearty.oura.models import AuthCodeRequest
from hearty.oura.storage import OuraUserAuthRepository, OuraUserInfoRepository
from hearty.utils.storage import PartitionKeyedDynamoRepository


class OuraUserAuthManager:
    @classmethod
    def build(cls, environment: str) -> OuraUserAuthManager:
        authorizer = OuraUserAuthorizer.build(environment)
        storage = OuraUserAuthRepository.build(environment)
        return cls(authorizer, storage)

    def __init__(self, authorizer: OuraUserAuthorizer, storage: OuraUserAuthRepository):
        self._authorizer = authorizer
        self._storage = storage

    def authorize_first_time(self, user_id: str, request: AuthCodeRequest) -> None:
        user_auth = self._authorizer.authorize_user(request.code, request.redirect_uri)
        self._storage.save_user_auth(user_id, user_auth)

    def refresh_authorization(self, user_id: str) -> None:
        existing_auth = self._storage.get_user_auth(user_id)
        if existing_auth is None:
            raise ValueError(f"Could not find auth for user {user_id}")

        new_auth = self._authorizer.refresh_user(existing_auth.refresh_token)
        self._storage.save_user_auth(user_id, new_auth)

    def get_user_auth(self, user_id: str) -> Optional[OuraUserAuth]:
        return self._storage.get_user_auth(user_id)


class OuraDataManager:
    @classmethod
    def build(cls, environment: str, user_id: str) -> OuraDataManager:

        user_auth_repo = OuraUserAuthManager.build(environment=environment)
        user_auth = user_auth_repo.get_user_auth(user_id)

        if user_auth is None:
            raise ValueError(f"Could not find auth for user {user_id}")

        return cls(
            OuraApiAccess.build(user_auth.access_token), OuraUserInfoRepository.build(environment)
        )

    def __init__(self, api: OuraApiAccess, user_info: OuraUserInfoRepository) -> None:
        self._api = api
        self._user_info = user_info

    def fetch_personal_info(
        self,
        patient: Patient,
    ) -> None:
        personal_info = self._api.get_personal_info()
        self._user_info.save_user_personal_info(patient.id, personal_info)
