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
FacetT = TypeVar("FacetT", bound=DatedBaseModel)


class HashKeyedRepository(ABC, Generic[ObjT]):
    @abstractmethod
    def save_item(self, item_id: str, item: ObjT) -> None:
        pass

    @abstractmethod
    def get_item(self, item_id: str) -> Optional[ObjT]:
        pass


class FacetKeyedRepository(ABC, Generic[ObjT, FacetT]):
    @abstractmethod
    def save_items(self, item_id: str, items: Iterable[ObjT]) -> None:
        pass

    @abstractmethod
    def get_items(self, item_id: str) -> Dict[FacetT, ObjT]:
        pass

    @abstractmethod
    def get_count(self, item_id: str) -> int:
        pass
