import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer

class CannonRush(sc2.BotAI):
    async def on_step(self, iteration: int):
        self.distribute_workers()

sc2.run_game(
    maps.get("AbyssalReefLe"),
    [Bot(Race.Protoss, CannonRush()), 
    Computer(Race.Terran, Difficulty.Easy)],
    realtime=True,
)