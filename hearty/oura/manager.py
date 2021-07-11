from __future__ import annotations

from typing import Optional
from hearty.models import Patient
from hearty.oura.api import OuraApiAccess, OuraUserAuthorizer, OuraUserAuth, PersonalInfo
from hearty.oura.constants import USER_KEY_ATTRIBUTE, USER_AUTH_TABLE_SUFFIX, USER_INFO_TABLE_SUFFIX
from hearty.oura.models import AuthCodeRequest
from hearty.utils.aws.dynamo import DynamoHashKeyedRepository
from hearty.utils.storage import HashKeyedRepository


class OuraUserAuthManager:
    @classmethod
    def build(cls, environment: str) -> OuraUserAuthManager:
        authorizer = OuraUserAuthorizer.build(environment)
        storage = DynamoHashKeyedRepository[OuraUserAuth].build(
            item_class=OuraUserAuth,
            key_attribute=USER_KEY_ATTRIBUTE,
            environment=environment,
            table_name=USER_AUTH_TABLE_SUFFIX,
        )
        return cls(authorizer, storage)

    def __init__(self, authorizer: OuraUserAuthorizer, storage: HashKeyedRepository[OuraUserAuth]):
        self._authorizer = authorizer
        self._storage = storage

    def authorize_first_time(self, user_id: str, request: AuthCodeRequest) -> None:
        user_auth = self._authorizer.authorize_user(request.code, request.redirect_uri)
        self._storage.save_item(user_id, user_auth)

    def refresh_authorization(self, user_id: str) -> None:
        existing_auth = self._storage.get_item(user_id)
        if existing_auth is None:
            raise ValueError(f"Could not find auth for user {user_id}")

        new_auth = self._authorizer.refresh_user(existing_auth.refresh_token)
        self._storage.save_item(user_id, new_auth)

    def get_user_auth(self, user_id: str) -> Optional[OuraUserAuth]:
        return self._storage.get_item(user_id)


class OuraDataManager:
    @classmethod
    def build(cls, environment: str, user_id: str) -> OuraDataManager:

        user_auth_repo = OuraUserAuthManager.build(environment=environment)
        user_auth = user_auth_repo.get_user_auth(user_id)

        if user_auth is None:
            raise ValueError(f"Could not find auth for user {user_id}")
        api = OuraApiAccess.build(user_auth.access_token)
        storage = DynamoHashKeyedRepository[PersonalInfo].build(
            item_class=PersonalInfo,
            key_attribute=USER_KEY_ATTRIBUTE,
            environment=environment,
            table_name=USER_INFO_TABLE_SUFFIX,
        )

        return cls(api, storage)

    def __init__(self, api: OuraApiAccess, user_info: HashKeyedRepository[PersonalInfo]) -> None:
        self._api = api
        self._user_info = user_info

    def fetch_personal_info(
        self,
        patient: Patient,
    ) -> None:
        personal_info = self._api.get_personal_info()
        self._user_info.save_item(patient.id, personal_info)
