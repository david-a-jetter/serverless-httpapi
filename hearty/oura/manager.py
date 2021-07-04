from __future__ import annotations

from typing import Optional
from hearty.models import Patient
from hearty.oura.api import OuraApiAccess, OuraUserAuthorizer
from hearty.oura.storage import AbstractOuraRepository, DynamoOuraRepository


class OuraUserAuthManager:
    @classmethod
    def build(cls, environment: str) -> OuraUserAuthManager:
        authorizer = OuraUserAuthorizer.build(environment)
        storage = DynamoOuraRepository.build(environment)
        return cls(authorizer, storage)

    def __init__(self, authorizer: OuraUserAuthorizer, storage: AbstractOuraRepository):
        self._authorizer = authorizer
        self._storage = storage

    def authorize_first_time(
        self, user_id: str, auth_code: str, redirect_uri: Optional[str]
    ) -> None:
        user_auth = self._authorizer.authorize_user(auth_code, redirect_uri)
        self._storage.save_user_auth(user_id, user_auth)

    def refresh_authorization(self, user_id: str) -> None:
        existing_auth = self._storage.get_user_auth(user_id)
        if existing_auth is None:
            raise ValueError(f"Could not find auth for user {user_id}")

        new_auth = self._authorizer.refresh_user(existing_auth.refresh_token)
        self._storage.save_user_auth(user_id, new_auth)


class OuraDataManager:
    @classmethod
    def build(cls, environment: str, user_id: str) -> OuraDataManager:

        repo = DynamoOuraRepository.build(environment)
        user = repo.get_user_auth(user_id)

        if user is None:
            raise ValueError(f"Could not find auth for user {user_id}")

        return cls(OuraApiAccess.build(user.access_token), DynamoOuraRepository.build(environment))

    def __init__(self, api: OuraApiAccess, storage: AbstractOuraRepository) -> None:
        self._api = api
        self._storage = storage

    def create_oura_user(
        self, patient: Patient, auth_code: str, redirect_uri: Optional[str]
    ) -> None:
        pass
