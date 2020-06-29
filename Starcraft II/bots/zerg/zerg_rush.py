import sc2
import random
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from sc2.constants import LARVA, DRONE, OVERLORD, HATCHERY, EXTRACTOR, QUEEN

class ZergRush(sc2.BotAI):
    async def on_step(self, iteration: int):
        await self.distribute_workers()
        await self.build_workers()
        await self.build_extractor()
        await self.build_supply()
        await self.build_queen()

    async def build_workers(self):
        for hatchery in self.units(HATCHERY).ready.idle:
            if self.can_afford(DRONE) and self.supply_workers < 16:
                self.do(hatchery.train(DRONE))

    async def build_supply(self):
        if self.supply_left < 10 and not self.already_pending(OVERLORD):
            hatchery = self.townhalls(HATCHERY).ready
            if hatchery.exists:
                if self.can_afford(OVERLORD):
                    self.train(OVERLORD, 1)

    async def build_queen(self):
        if not self.already_pending(QUEEN) and self.units(QUEEN).amount <= 2:
            hatchery = self.townhalls(HATCHERY).exists
            if self.can_afford(QUEEN) and hatchery:
                self.do(hatchery.train(QUEEN))

    async def build_extractor(self):
        if not self.structures(EXTRACTOR) and self.structures(EXTRACTOR).amount < 1:
            if self.can_afford(EXTRACTOR):
                drone = self.workers.random
                target = self.vespene_geyser.closest_to(drone)
                drone.build_gas(target)


sc2.run_game(
    maps.get("AbyssalReefLe"),
    [Bot(Race.Zerg, ZergRush()), 
    Computer(Race.Terran, Difficulty.Easy)],
    realtime=False,
)