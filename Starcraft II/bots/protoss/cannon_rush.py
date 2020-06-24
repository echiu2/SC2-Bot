import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from sc2.constants import NEXUS, PROBE, PYLON

class CannonRush(sc2.BotAI):
    async def on_step(self, iteration: int):
        await self.distribute_workers()
        await self.build_workers()
        await self.build_supply()
    
    async def build_workers(self):
        for nexus in self.townhalls(NEXUS).ready.idle:
            if self.can_afford(PROBE) and self.supply_workers < 16:
                nexus.train(PROBE)

    async def build_supply(self):
        if self.supply_left < 5 and not self.already_pending(PYLON):
            nexus = self.townhalls(NEXUS).ready
            if nexus.exists:
                if self.can_afford(PYLON):
                    await self.build(PYLON, near=nexus.first)
                    


sc2.run_game(
    maps.get("AbyssalReefLe"),
    [Bot(Race.Protoss, CannonRush()), 
    Computer(Race.Terran, Difficulty.Easy)],
    realtime=False,
)