import sc2
import random
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from sc2.constants import LARVA, DRONE, OVERLORD, HATCHERY, EXTRACTOR, QUEEN, SPAWNINGPOOL

class ZergRush(sc2.BotAI):

    def __init__(self):
        self.gas_workers = None

    async def on_step(self, iteration: int):
        await self.distribute_workers()
        await self.build_workers()
        await self.build_extractor()
        await self.get_gas()
        await self.build_supply()
        await self.build_offensive_force()
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

    async def build_offensive_force(self):
        if not self.structures(SPAWNINGPOOL) and not self.already_pending(SPAWNINGPOOL):
            if self.can_afford(SPAWNINGPOOL):
                hatchery = self.townhalls[0]
                for d in range(4, 15):
                    pos = hatchery.position.towards(self.game_info.map_center, d)
                    drone = self.workers.closest_to(pos)
                    self.do(drone.build(SPAWNINGPOOL, pos))


    async def get_gas(self):
        if self.structures(EXTRACTOR).ready.exists and not self.gas_workers:
            extractor = self.gas_buildings.first
            self.gas_workers = self.workers.random_group_of(3)
            for drone in self.gas_workers:
                if extractor:
                    self.do(drone.gather(target=extractor, queue=True))

    async def build_queen(self):
        if self.structures(SPAWNINGPOOL).ready.exists:
            if not self.already_pending(QUEEN) and self.units(QUEEN).amount <= 2:
                if self.can_afford(QUEEN):
                    self.train(QUEEN)

    async def build_extractor(self):
        if not self.structures(EXTRACTOR) or self.structures(EXTRACTOR).amount <= 1:
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