from itertools import cycle

from core.storage import storage


class GamersGenerator:
    def __init__(self):
        self._gamers = self.pass_turn()

    @staticmethod
    async def pass_turn():
        for gamer in cycle(await storage.get_or_create("gamers", [])):
            yield gamer

    async def regenerate(self):
        """Regenerates generator"""
        self._gamers = self.pass_turn()

    async def next(self):
        return await self._gamers.__anext__()


gamers = GamersGenerator()
