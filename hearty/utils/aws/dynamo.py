from __future__ import annotations

import logging
from io import StringIO
from datetime import date
import boto3
from boto3.dynamodb.conditions import Key
from typing import Generic, Optional, Dict, Iterable
from pydantic import BaseModel

from hearty.utils.storage import HashKeyedRepository, ObjT, DateKeyedRepository, DatedObjT

logger = logging.getLogger(__name__)


class PartitionKeyedDynamoRepository(HashKeyedRepository[ObjT]):
    @classmethod
    def build(
        cls, key_attribute: str, environment: str, table_name: str
    ) -> PartitionKeyedDynamoRepository[Generic[ObjT]]:
        resource = boto3.resource("dynamodb")
        return cls(key_attribute, _build_table(environment, table_name, resource))

    def __init__(self, key_attribute: str, table):
        self._key_attribute = key_attribute
        self._table = table

    def save_item(self, item_id: str, item: ObjT) -> None:
        logger.info(
            "Saving item to partition keyed table",
            extra={"table_name": self._table.table_name, "item_id": item_id},
        )
        item = {self._key_attribute: item_id, **item.dict()}
        self._table.put_item(Item=item)

    def get_item(self, item_id: str) -> Optional[ObjT]:
        logger.info(
            "Getting item from partition keyed table",
            extra={"table_name": self._table.table_name, "item_id": item_id},
        )
        key = {self._key_attribute: item_id}
        response = self._table.get_item(Key=key)
        item = response.get("Item")

        if item:
            return type(ObjT)(**item)
        else:
            return None


class DateKeyedDynamoRepository(DateKeyedRepository[DatedObjT]):
    @classmethod
    def build(
        cls, key_attribute: str, environment: str, table_name: str
    ) -> DateKeyedDynamoRepository[Generic[DatedObjT]]:
        resource = boto3.resource("dynamodb")
        return cls(key_attribute, _build_table(environment, table_name, resource))

    def __init__(self, key_attribute: str, table):
        self._key_attribute = key_attribute
        self._table = table

    def save_items(self, item_id: str, items: Iterable[DatedObjT]) -> None:
        logger.info(
            "Saving items to date keyed table",
            extra={"table_name": self._table.table_name, "partition_key_id": item_id},
        )
        with self._table.batch_writer() as batch:
            for item in items:
                item = {
                    self._key_attribute: item_id,
                    "date": item.date_key,
                    **item.dict(exclude={"date"}),
                }
                batch.put_item(Item=item)

    def get_items(self, item_id: str) -> Dict[date, DatedObjT]:
        logger.info(
            "Getting items from date keyed table",
            extra={"table_name": self._table.table_name, "partition_key_id": item_id},
        )

        response = self._table.query(KeyConditionExpression=Key(self._key_attribute).eq(item_id))
        keyed_items = {}
        for item in response["Items"]:
            model_object = type(DatedObjT)(**item)
            keyed_items[model_object.date_key] = model_object

        return keyed_items

    def get_count(self, item_id: str) -> int:
        raise NotImplementedError()


def _build_table(prefix: str, suffix: str, resource):
    table_name = f"{prefix}-{suffix}"
    table = resource.Table(table_name)
    return table


class UpdateItemArguments(BaseModel):
    update_expression: str
    attribute_names: Dict[str, str]
    attribute_values: Dict[str, str]


def build_update_item_arguments(item: Dict[str, str]) -> UpdateItemArguments:
    update_expression = StringIO()
    names = {}
    values = {}

    count = 0
    for k, v in item.items():
        attr_name = f"#{k}"
        attr_value = f"val{count}"
        prefixed_value = f":{attr_value}"
        if count == 0:
            update_expression.write("SET ")
        else:
            update_expression.write(", ")

        update_expression.write(f"{attr_name} = prefixed_value")
        names[attr_name] = attr_value
        values[prefixed_value] = v

        count += 1

    arguments = UpdateItemArguments(
        update_expression=update_expression.getvalue(),
        attribute_names=names,
        attribute_values=values,
    )

    return arguments
