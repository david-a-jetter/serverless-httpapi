from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from typing import Optional, Dict, Type

import boto3
from boto3.dynamodb.conditions import Key
from pydantic import BaseModel

from hearty.oura.api import PersonalInfo, Readiness, Sleep, Activity, IdealBedtime, DatedBaseModel
from hearty.oura.constants import (
    USER_TABLE_SUFFIX,
    READINESS_TABLE_SUFFIX,
    SLEEP_TABLE_SUFFIX,
    ACTIVITY_TABLE_SUFFIX,
    BEDTIME_TABLE_SUFFIX,
)


class AbstractOuraRepository(ABC):
    @abstractmethod
    def save_user_info(self, user_id: str, info: PersonalInfo) -> None:
        pass

    @abstractmethod
    def get_user_info(self, user_id: str) -> Optional[PersonalInfo]:
        pass

    @abstractmethod
    def save_readiness(self, user_id: str, readiness: Dict[date, Readiness]) -> None:
        pass

    @abstractmethod
    def get_readiness(self, user_id: str) -> Dict[date, Readiness]:
        pass

    @abstractmethod
    def save_sleep(self, user_id: str, sleep: Dict[date, Sleep]) -> None:
        pass

    @abstractmethod
    def get_sleep(self, user_id: str) -> Dict[date, Sleep]:
        pass

    @abstractmethod
    def save_activity(self, user_id: str, activity: Dict[date, Activity]) -> None:
        pass

    @abstractmethod
    def get_activity(self, user_id: str) -> Dict[date, Activity]:
        pass

    @abstractmethod
    def save_bedtime(self, user_id: str, bedtime: Dict[date, IdealBedtime]) -> None:
        pass

    @abstractmethod
    def get_bedtime(self, user_id: str) -> Dict[date, IdealBedtime]:
        pass


class DynamoOuraRepository(AbstractOuraRepository):
    @classmethod
    def build(cls, table_prefix: str) -> DynamoOuraRepository:
        resource = boto3.resource("dynamodb")
        return cls(
            cls._build_table(table_prefix, USER_TABLE_SUFFIX, resource),
            cls._build_table(table_prefix, READINESS_TABLE_SUFFIX, resource),
            cls._build_table(table_prefix, SLEEP_TABLE_SUFFIX, resource),
            cls._build_table(table_prefix, ACTIVITY_TABLE_SUFFIX, resource),
            cls._build_table(table_prefix, BEDTIME_TABLE_SUFFIX, resource),
        )

    @classmethod
    def _build_table(cls, prefix: str, suffix: str, resource):
        table_name = f"{prefix}-{suffix}"
        table = resource.Table(table_name)
        return table

    def __init__(
        self, user_table, readiness_table, sleep_table, activity_table, bedtime_table
    ) -> None:
        self._users = user_table
        self._readiness = readiness_table
        self._sleep = sleep_table
        self._activity = activity_table
        self._bedtime = bedtime_table

    def save_user_info(self, user_id: str, info: PersonalInfo) -> None:

        item = {"user_id": user_id, **info.dict()}
        self._users.put_item(Item=item)

    def get_user_info(self, user_id: str) -> Optional[PersonalInfo]:
        key = {"user_id": user_id}
        response = self._users.get_item(Key=key)
        item = response.get("Item")

        if item:
            return PersonalInfo(**item)
        else:
            return None

    def save_readiness(self, user_id: str, readiness: Dict[date, Readiness]) -> None:
        self._save_date_keyed_items(user_id, readiness, self._readiness)

    def get_readiness(self, user_id: str) -> Dict[date, Readiness]:
        return self._get_user_keyed_items(user_id, Readiness, self._readiness)

    def save_sleep(self, user_id: str, sleep: Dict[date, Sleep]) -> None:
        self._save_date_keyed_items(user_id, sleep, self._sleep)

    def get_sleep(self, user_id: str) -> Dict[date, Sleep]:
        return self._get_user_keyed_items(user_id, Sleep, self._sleep)

    def save_activity(self, user_id: str, activity: Dict[date, Activity]) -> None:
        self._save_date_keyed_items(user_id, activity, self._activity)

    def get_activity(self, user_id: str) -> Dict[date, Activity]:
        return self._get_user_keyed_items(user_id, Activity, self._activity)

    def save_bedtime(self, user_id: str, bedtime: Dict[date, IdealBedtime]) -> None:
        self._save_date_keyed_items(user_id, bedtime, self._bedtime)

    def get_bedtime(self, user_id: str) -> Dict[date, IdealBedtime]:
        return self._get_user_keyed_items(user_id, IdealBedtime, self._bedtime)

    @staticmethod
    def _save_date_keyed_items(user_id: str, items: Dict[date, BaseModel], table) -> None:
        with table.batch_writer() as batch:
            for date_key, model_object in items.items():
                item = {"user_id": user_id, "date": date_key, **model_object.dict()}
                batch.put_item(Item=item)

    @staticmethod
    def _get_user_keyed_items(
        user_id: str, model_class: Type[DatedBaseModel], table
    ) -> Dict[date, DatedBaseModel]:
        response = table.query(KeyConditionExpression=Key("user_id").eq(user_id))

        keyed_items = {}
        for item in response["Items"]:
            model_object = model_class(**item)
            keyed_items[model_object.date_key] = model_object

        return keyed_items
