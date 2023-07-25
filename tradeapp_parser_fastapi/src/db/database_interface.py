from abc import ABC, abstractmethod
from typing import List

from pydantic import BaseModel


class DatabaseInterface(ABC):
    @abstractmethod
    async def save_item(self, item: BaseModel) -> str:
        pass

    @abstractmethod
    async def get_items(self, **kwargs) -> List[BaseModel]:
        pass

    @abstractmethod
    async def item_exists(self, **kwargs):
        pass

    @abstractmethod
    async def update_item(self, **kwargs):
        pass

    @abstractmethod
    async def delete_item(self, **kwargs):
        pass
