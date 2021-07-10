from __future__ import annotations

import logging
from abc import abstractmethod, ABC
from io import StringIO
from datetime import date
import boto3
from boto3.dynamodb.conditions import Key
from typing import TypeVar, Generic, Type, Optional, Dict, Iterable
from pydantic import BaseModel


logger = logging.getLogger(__name__)


class DatedBaseModel(ABC, BaseModel):
    @property
    @abstractmethod
    def date_key(self) -> date:
        pass


T = TypeVar("T", bound=BaseModel)
DT = TypeVar("DT", bound=DatedBaseModel)


class PartitionKeyedDynamoRepository(Generic[T]):
    @classmethod
    def build(
        cls, key_attribute: str, environment: str, table_name: str
    ) -> PartitionKeyedDynamoRepository[Generic[T]]:
        resource = boto3.resource("dynamodb")
        return cls(key_attribute, _build_table(environment, table_name, resource))

    def __init__(self, key_attribute: str, table):
        self._key_attribute = key_attribute
        self._table = table

    def save_item(self, item_id: str, item: T) -> None:
        self._save_partition_keyed_item(self._key_attribute, item_id, item, self._table)

    def get_item(self, item_id: str) -> Optional[T]:
        return self._get_partition_keyed_item(self._key_attribute, item_id, T, self._table)

    @staticmethod
    def _save_partition_keyed_item(
        key_attribute: str, item_id: str, model_object: BaseModel, table
    ) -> None:
        logger.info(
            "Saving item to partition keyed table",
            extra={"table_name": table.table_name, "item_id": item_id},
        )
        item = {key_attribute: item_id, **model_object.dict()}
        table.put_item(Item=item)

    @staticmethod
    def _get_partition_keyed_item(
        key_attribute: str, item_id: str, model_class: Type[BaseModel], table
    ) -> Optional[BaseModel]:
        logger.info(
            "Getting item from partition keyed table",
            extra={"table_name": table.table_name, "item_id": item_id},
        )
        key = {key_attribute: item_id}
        response = table.get_item(Key=key)
        item = response.get("Item")

        if item:
            return model_class(**item)
        else:
            return None


class DateKeyedDynamoRepository(Generic[DT]):
    @classmethod
    def build(
        cls, key_attribute: str, environment: str, table_name: str
    ) -> DateKeyedDynamoRepository[Generic[DT]]:
        resource = boto3.resource("dynamodb")
        return cls(key_attribute, _build_table(environment, table_name, resource))

    def __init__(self, key_attribute: str, table):
        self._key_attribute = key_attribute
        self._table = table

    def save_items(self, item_id: str, items: Iterable[DT]) -> None:
        _save_date_keyed_items(self._key_attribute, item_id, items, self._table)

    def get_items(self, item_id: str) -> Dict[date, DT]:
        return _get_user_keyed_items(self._key_attribute, item_id, Type[DT], self._table)


def _build_table(prefix: str, suffix: str, resource):
    table_name = f"{prefix}-{suffix}"
    table = resource.Table(table_name)
    return table


def _save_date_keyed_items(key_attribute: str, item_id: str, items: Iterable[DT], table) -> None:
    logger.info(
        "Saving items to date keyed table",
        extra={"table_name": table.table_name, "partition_key_id": item_id},
    )
    with table.batch_writer() as batch:
        for item in items:
            item = {key_attribute: item_id, "date": item.date_key, **item.dict(exclude="date")}
            batch.put_item(Item=item)


def _get_user_keyed_items(
    key_attribute: str, item_id: str, model_class: Type[DT], table
) -> Dict[date, DT]:

    logger.info(
        "Getting items from date keyed table",
        extra={"table_name": table.table_name, "partition_key_id": item_id},
    )

    response = table.query(KeyConditionExpression=Key(key_attribute).eq(item_id))
    keyed_items = {}
    for item in response["Items"]:
        model_object = model_class(**item)
        keyed_items[model_object.date_key] = model_object

    return keyed_items


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
