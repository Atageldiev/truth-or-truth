from aiogram.types import Chat, User

from .conf import dp


class Storage:
    def __init__(self):
        self._storage = dp.storage

    @property
    def chat(self):
        return Chat.get_current()

    @property
    def user(self):
        return User.get_current()

    async def set(self, data):
        """Put `data` as a storage data"""
        await self._storage.set_data(chat=self.chat.id, data=data)

    async def all(self):
        return await self._storage.get_data(chat=self.chat.id)

    async def update(self, data: dict):
        storage_data = await self.all()
        storage_data.update(data)
        await self.set(storage_data)

    async def get(self, key):
        data = await self.all()
        return data[key]

    async def get_or_create(self, key, value):
        data = await self.all()
        if key not in data:
            data[key] = value
            await self.update(data)
            return value

        return data[key]

    async def increment(self, key):
        data = await self.all()
        if not isinstance(data[key], int):
            raise TypeError(f"Value of `{key}` is not integer")

        data.update({key: data[key] + 1})

    async def clear(self):
        await self.set({})


storage = Storage()
