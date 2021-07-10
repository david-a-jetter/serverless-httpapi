from abc import ABC, abstractmethod
from datetime import date
from typing import Generic, TypeVar, Optional, Iterable, Dict

from pydantic import BaseModel


class DatedBaseModel(ABC, BaseModel):
    @property
    @abstractmethod
    def date_key(self) -> date:
        pass


ObjT = TypeVar("ObjT", bound=BaseModel)
DatedObjT = TypeVar("DatedObjT", bound=DatedBaseModel)


class HashKeyedRepository(ABC, Generic[ObjT]):
    @abstractmethod
    def save_item(self, item_id: str, item: ObjT) -> None:
        pass

    @abstractmethod
    def get_item(self, item_id: str) -> Optional[ObjT]:
        pass


class DateKeyedRepository(ABC, Generic[DatedObjT]):
    @abstractmethod
    def save_items(self, item_id: str, items: Iterable[DatedObjT]) -> None:
        pass

    @abstractmethod
    def get_items(self, item_id: str) -> Dict[date, DatedObjT]:
        pass

    @abstractmethod
    def get_count(self, item_id: str) -> int:
        pass
