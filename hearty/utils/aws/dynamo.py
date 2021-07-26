from __future__ import annotations

import logging
from io import StringIO
import boto3
from boto3.dynamodb.conditions import Key
from typing import Optional, Dict, Iterable, Type
from pydantic import BaseModel

from hearty.utils.storage import HashKeyedRepository, ObjT, FacetT, FacetKeyedRepository

logger = logging.getLogger(__name__)


class DynamoHashKeyedRepository(HashKeyedRepository[ObjT]):
    @classmethod
    def build(
        cls, item_class: Type[ObjT], key_attribute: str, environment: str, table_name: str
    ) -> DynamoHashKeyedRepository[ObjT]:
        resource = boto3.resource("dynamodb")
        return cls(item_class, key_attribute, _build_table(environment, table_name, resource))

    def __init__(self, item_class: Type[ObjT], key_attribute: str, table):
        self._item_class = item_class
        self._key_attribute = key_attribute
        self._table = table

    def save_item(self, item_id: str, item: ObjT) -> None:
        logger.info(
            "Saving item to partition keyed table",
            extra={"table_name": self._table.table_name, "item_id": item_id},
        )
        put_item = {self._key_attribute: item_id, **item.dict()}
        self._table.put_item(Item=put_item)

    def get_item(self, item_id: str) -> Optional[ObjT]:
        logger.info(
            "Getting item from partition keyed table",
            extra={"table_name": self._table.table_name, "item_id": item_id},
        )
        key = {self._key_attribute: item_id}
        response = self._table.get_item(Key=key)
        item = response.get("Item")

        if item:
            return self._item_class(**item)
        else:
            return None


class DynamoFacetKeyedRepository(FacetKeyedRepository[ObjT, FacetT]):
    @classmethod
    def build(
        cls,
        item_class: Type[ObjT],
        key_attribute: str,
        facet_attribute: str,
        environment: str,
        table_name: str,
    ) -> DynamoFacetKeyedRepository[ObjT, FacetT]:
        resource = boto3.resource("dynamodb")
        return cls(
            item_class,
            key_attribute,
            facet_attribute,
            _build_table(environment, table_name, resource),
        )

    def __init__(
        self,
        item_class: Type[ObjT],
        key_attribute: str,
        facet_attribute: str,
        table,
    ):
        self._item_class = item_class
        self._key_attribute = key_attribute
        self._facet_attribute = facet_attribute
        self._table = table

    def save_items(self, item_id: str, items: Iterable[ObjT]) -> None:
        logger.info(
            "Saving items to facet keyed table",
            extra={"table_name": self._table.table_name, "partition_key_id": item_id},
        )
        with self._table.batch_writer() as batch:
            for item in items:
                item_dict = item.dict()
                facet_attribute = item_dict.pop(self._facet_attribute)
                put_item = {
                    self._key_attribute: item_id,
                    self._facet_attribute: facet_attribute,
                    **item_dict,
                }
                batch.put_item(Item=put_item)

    def get_items(self, item_id: str) -> Dict[FacetT, ObjT]:
        logger.info(
            "Getting items from facet keyed table",
            extra={"table_name": self._table.table_name, "partition_key_id": item_id},
        )

        response = self._table.query(KeyConditionExpression=Key(self._key_attribute).eq(item_id))
        keyed_items = {}
        for item in response["Items"]:
            model_object = self._item_class(**item)
            keyed_items[getattr(model_object, self._facet_attribute)] = model_object

        return keyed_items

    def get_count(self, item_id: str) -> int:
        logger.info(
            "Getting count of items from facet keyed table",
            extra={"table_name": self._table.table_name, "partition_key_id": item_id},
        )

        response = self._table.query(
            Select="COUNT", KeyConditionExpression=Key(self._key_attribute).eq(item_id)
        )

        count = int(response["Count"])

        return count


def _build_table(prefix: str, suffix: str, resource):
    table_name = f"{prefix}-{suffix}"
    table = resource.Table(table_name)
    return table


class UpdateItemArguments(BaseModel):
    update_expression: str
    attribute_names: Dict[str, str]
    attribute_values: Dict[str, str]


# TODO: Add tests to this if/when it starts being used
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
