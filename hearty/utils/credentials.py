from typing import Optional
from pydantic import BaseModel
from hearty.utils.aws.dynamo import PartitionKeyedDynamoRepository


TABLE_KEY_ATTRIBUTE = "app_name"
TABLE_NAME_SUFFIX = "secrets"


class Credential(BaseModel):
    client_id: Optional[str]
    client_secret: Optional[str]


class CredentialsRepository:
    @classmethod
    def build(cls, environment: str):
        dynamo = PartitionKeyedDynamoRepository[Credential](
            key_attribute=TABLE_KEY_ATTRIBUTE,
            environment=environment,
            table_name=TABLE_NAME_SUFFIX,
        )
        return cls(dynamo)

    def __init__(self, repo: PartitionKeyedDynamoRepository[Credential]):
        self._repo = repo

    def save_user_auth(self, user_id: str, auth: Credential) -> None:
        self._repo.save_item(user_id, auth)

    def get_user_auth(self, user_id) -> Optional[Credential]:
        return self._repo.get_item(user_id)
