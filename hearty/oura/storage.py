from typing import Optional

from hearty.oura.api import OuraUserAuth, PersonalInfo
from hearty.oura.constants import USER_KEY_ATTRIBUTE, USER_AUTH_TABLE_SUFFIX, USER_INFO_TABLE_SUFFIX
from hearty.utils.storage import PartitionKeyedDynamoRepository


class OuraUserAuthRepository:
    @classmethod
    def build(cls, environment: str):
        dynamo = PartitionKeyedDynamoRepository[OuraUserAuth](
            key_attribute=USER_KEY_ATTRIBUTE,
            environment=environment,
            table_name=USER_AUTH_TABLE_SUFFIX,
        )
        return cls(dynamo)

    def __init__(self, repo: PartitionKeyedDynamoRepository[OuraUserAuth]):
        self._repo = repo

    def save_user_auth(self, user_id: str, auth: OuraUserAuth) -> None:
        self._repo.save_item(user_id, auth)

    def get_user_auth(self, user_id) -> Optional[OuraUserAuth]:
        return self._repo.get_item(user_id)


class OuraUserInfoRepository:
    @classmethod
    def build(cls, environment: str):
        dynamo = PartitionKeyedDynamoRepository[PersonalInfo](
            key_attribute=USER_KEY_ATTRIBUTE,
            environment=environment,
            table_name=USER_INFO_TABLE_SUFFIX,
        )
        return cls(dynamo)

    def __init__(self, repo: PartitionKeyedDynamoRepository[PersonalInfo]):
        self._repo = repo

    def save_user_personal_info(self, user_id: str, personal_info: PersonalInfo) -> None:
        self._repo.save_item(user_id, personal_info)

    def get_user_personal_info(self, user_id) -> Optional[PersonalInfo]:
        return self._repo.get_item(user_id)
