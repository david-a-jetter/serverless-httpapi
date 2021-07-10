from typing import Optional
from pydantic import BaseModel
from hearty.utils.aws.dynamo import PartitionKeyedDynamoRepository
from hearty.utils.storage import HashKeyedRepository

TABLE_KEY_ATTRIBUTE = "app_name"
TABLE_NAME_SUFFIX = "secrets"


class Credential(BaseModel):
    client_id: Optional[str]
    client_secret: Optional[str]


def build_credentials_repo(environment: str) -> HashKeyedRepository[Credential]:
    return PartitionKeyedDynamoRepository[Credential](
        key_attribute=TABLE_KEY_ATTRIBUTE,
        environment=environment,
        table_name=TABLE_NAME_SUFFIX,
    )
