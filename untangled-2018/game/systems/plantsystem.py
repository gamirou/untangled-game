import math

from lib.system import System
from game.components import *
from game.entities import *
import pygame
import time

class PlantSystem(System):
    last_plant = 0
    colplants = []
    def enablePlant(self, key):
        self.colplants.append(key)
    def disablePlant(self, key):
        if key in self.colplants:
            self.colplants.remove(key)

    def update(self, game, dt, events):
        if game.net.is_hosting():
            for key,entity in game.entities.items():
                if Crops in entity:
                    crops = entity[Crops]
                    spritesheet = entity[SpriteSheet]
                    water_bar = entity[WaterBar]
                    growth_bar = entity[Energy]
                    plantedTime = crops.plantage_time
                    timeDifference = time.time() - plantedTime

                    water_bar.value = max(water_bar.value-0.005, 1)

                    # Time to grow is inversely proportional to water bar value
                    if timeDifference > (1/(water_bar.value))*60*60*crops.growth_stage:
                        crops.growth_stage = min(crops.growth_stage+1, crops.max_growth_stage)

                    growth_bar.value = (timeDifference / (1 / water_bar.value * 60 * 60 * (crops.growth_stage or 1))) * 100

                    spritesheet.default_tile = crops.growth_stage

            # Handle game actions
            for key,entity in dict(game.entities).items():
                if GameAction in entity and IngameObject in entity:
                    action = entity[GameAction]
                    if action.action == 'plant' and action.last_plant + 2 < time.time():
                        io = entity[IngameObject]
                        game.add_entity(create_plant(game, "wheat", "assets/sprites/wheat.png", io.position))
                        action.action = ''
                        action.last_plant = time.time()
                    if action.action == 'water':
                        for k,e in dict(game.entities).items():
                            if Crops in e:
                                if entity[IngameObject].get_rect().colliderect(e[IngameObject].get_rect()):
                                    water_bar = e[WaterBar]
                                    water_bar.value = min(water_bar.value + 0.2, 100)
                                    action.action = ''
                    if action.action == 'harvest':
                        for k,e in dict(game.entities).items():
                            if Crops in e:
                                if e[Crops].growth_stage >= e[Crops].max_growth_stage:
                                    # Are the entity and the player touching?
                                    if entity[IngameObject].get_rect().colliderect(e[IngameObject].get_rect()):
                                        item_igo = IngameObject(position=entity[IngameObject].get_rect().topleft,size=(64,64))
                                        item_ss = SpriteSheet(
                                            path = 'assets/sprites/debug.png',
                                            tile_size = 64,
                                            tiles={
                                                'default':[0]
                                            },
                                            moving=False
                                        )
                                        game.add_entity(create_item(item_igo,item_ss))
                                        action.action = ''


