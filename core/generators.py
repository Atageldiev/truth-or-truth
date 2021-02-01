from itertools import cycle

from core.storage import storage


class GamersGenerator:
    def __init__(self):
        self._generator = self._generate()

    async def _generate(self):
        for gamer in cycle(await self._get_gamers_list()):
            yield gamer

    @staticmethod
    async def _get_gamers_list():
        return await storage.get_or_create("gamers", [])

    async def regenerate(self):
        """Regenerates generator"""
        self._generator = self._generate()

    async def next(self):
        return await self._generator.__anext__()


gamers = GamersGenerator()
