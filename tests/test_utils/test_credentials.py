from unittest.mock import patch, MagicMock

from faker import Faker

from hearty.utils.credentials import build_credentials_repo, Credential

fake = Faker()


@patch("hearty.utils.aws.dynamo.boto3")
def test_build_credentials_repo(boto3):
    table = MagicMock()
    resource = MagicMock()
    resource.Table.return_value = table
    boto3.resource.return_value = resource
    environment = fake.bothify()
    repo = build_credentials_repo(environment)

    assert repo._item_class == Credential
    assert repo._key_attribute == "app_name"
    assert repo._table == table

    args, kwargs = resource.Table.call_args
    assert args[0] == f"{environment}-Secrets"
