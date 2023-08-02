from abc import abstractmethod
from typing import List

from pydantic import BaseModel


class DatabaseManager(object):

    @property
    def client(self):
        raise NotImplementedError

    @property
    def db(self):
        raise NotImplementedError

    @abstractmethod
    async def save_item(self, item: BaseModel):
        pass

    @abstractmethod
    async def save_items(self, **kwargs):
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
