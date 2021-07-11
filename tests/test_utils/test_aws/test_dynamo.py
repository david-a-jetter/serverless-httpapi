from unittest.mock import patch, MagicMock
from uuid import uuid4

from faker import Faker

from hearty.utils.aws.dynamo import DynamoHashKeyedRepository, DynamoFacetKeyedRepository
from tests.models import ExtraModel

fake = Faker()


@patch("hearty.utils.aws.dynamo.boto3")
def test_hash_keyed_repo_build(boto3):
    item_class = ExtraModel
    table = MagicMock()
    resource = MagicMock()
    resource.Table.return_value = table
    boto3.resource.return_value = resource
    key_attr = fake.bothify()
    environment = fake.bothify()
    table_name = fake.bothify()
    repo = DynamoHashKeyedRepository.build(item_class, key_attr, environment, table_name)

    assert repo._item_class == item_class
    assert repo._key_attribute == key_attr
    assert repo._table == table

    args, kwargs = resource.Table.call_args
    assert args[0] == f"{environment}-{table_name}"


def test_hash_keyed_save_item():
    key_attr = fake.bothify()
    table = MagicMock()
    repo = DynamoHashKeyedRepository[ExtraModel](ExtraModel, key_attr, table)
    item_id = fake.bothify()
    item = MagicMock()
    item.dict.return_value = fake.pydict()

    repo.save_item(item_id, item)
    args, kwargs = table.put_item.call_args

    put_item = kwargs["Item"]
    assert put_item[key_attr] == item_id
    del put_item[key_attr]
    assert put_item == item.dict()


def test_hash_keyed_get_item_exists():
    key_attr = fake.bothify()
    table = MagicMock()
    repo = DynamoHashKeyedRepository[ExtraModel](ExtraModel, key_attr, table)
    item_id = fake.bothify()
    item_values = fake.pydict()
    item = ExtraModel(**item_values)
    table.get_item.return_value = {"Item": item.dict()}

    actual = repo.get_item(item_id)
    args, kwargs = table.get_item.call_args

    assert kwargs["Key"] == {key_attr: item_id}
    assert actual == item


def test_hash_keyed_get_item_not_exists():
    key_attr = fake.bothify()
    table = MagicMock()
    repo = DynamoHashKeyedRepository[ExtraModel](ExtraModel, key_attr, table)
    table.get_item.return_value = {"Item": None}

    actual = repo.get_item(MagicMock())

    assert actual is None


@patch("hearty.utils.aws.dynamo.boto3")
def test_facet_keyed_repo_build(boto3):
    item_class = ExtraModel
    table = MagicMock()
    resource = MagicMock()
    resource.Table.return_value = table
    boto3.resource.return_value = resource
    key_attr = fake.bothify()
    facet_attribute = fake.bothify()
    environment = fake.bothify()
    table_name = fake.bothify()

    repo = DynamoFacetKeyedRepository.build(
        item_class, key_attr, facet_attribute, environment, table_name
    )

    assert repo._item_class == item_class
    assert repo._key_attribute == key_attr
    assert repo._facet_attribute == facet_attribute
    assert repo._table == table

    args, kwargs = resource.Table.call_args
    assert args[0] == f"{environment}-{table_name}"


def test_facet_keyed_repo_save_items():
    item_class = ExtraModel
    key_attr = fake.bothify()
    facet_attr = fake.bothify()
    table = MagicMock()
    writer = MagicMock()
    table.batch_writer.return_value.__enter__.return_value = writer

    repo = DynamoFacetKeyedRepository(item_class, key_attr, facet_attr, table)

    item_id = fake.bothify()
    count = 10
    items = [ExtraModel(**{facet_attr: MagicMock(), **fake.pydict()}) for _ in range(0, count)]
    repo.save_items(item_id, items)

    calls = writer.put_item.call_args_list

    assert len(calls) == count

    actual_items = [kwargs["Item"] for args, kwargs in calls]

    for item in items:
        item_dict = item.dict()
        facet = item_dict.pop(facet_attr)
        expected_item = {key_attr: item_id, facet_attr: facet, **item_dict}
        assert expected_item in actual_items


def test_facet_keyed_repo_get_items():
    item_id = fake.bothify()
    item_class = ExtraModel
    key_attr = fake.bothify()
    facet_attr = fake.bothify()
    table = MagicMock()
    count = 10
    return_items = []
    for _ in range(0, count):
        item_dict = fake.pydict()
        item_dict[facet_attr] = str(uuid4())
        item = ExtraModel(**item_dict)
        return_items.append(item)
    table.query.return_value = {"Items": [item.dict() for item in return_items]}

    repo = DynamoFacetKeyedRepository(item_class, key_attr, facet_attr, table)
    actuals = repo.get_items(item_id)

    args, kwargs = table.query.call_args

    expression = kwargs["KeyConditionExpression"]
    assert expression.expression_operator == "="
    assert expression._values[0].name == key_attr
    assert expression._values[1] == item_id

    assert len(actuals) == len(return_items)
    for expected in return_items:
        actual = actuals[expected.dict()[facet_attr]]
        assert actual == expected


def test_facet_keyed_repo_get_count():
    item_id = fake.bothify()
    key_attr = fake.bothify()
    table = MagicMock()
    count = fake.pyint()
    table.query.return_value = {"Count": count}

    repo = DynamoFacetKeyedRepository(MagicMock, key_attr, MagicMock(), table)
    actual_count = repo.get_count(item_id)

    assert actual_count == count
    args, kwargs = table.query.call_args
    assert kwargs["Select"] == "COUNT"
    expression = kwargs["KeyConditionExpression"]
    assert expression.expression_operator == "="
    assert expression._values[0].name == key_attr
    assert expression._values[1] == item_id
