from lib.system import System
from game.components import *
import pygame
import time
class PlantSystem(System):
    def update(self, game, dt, events):
        for key,entity in game.entities.items():
            if Crops in entity:
                crops = entity[Crops]
                spritesheet = entity[SpriteSheet]
                health = entity[Health]
                plantedTime = crops.plantage_time          
                timeDifference = time.time() - plantedTime

                # Get the health value
                # Use the health value to determine when the growth stage should be changed
                if 10 < health.value < 40 :
                    crops.growth_stage = 0
                elif 40 < health.value < 60:
                    crops.growth_stage = 1
                elif 60 < health.value < 80:
                    crops.growth_stage = 2
                elif health.value > 100:
                    crops.growth_stage = 3
                if health.value > 100:
                    health.value = 101
                
                spritesheet.default_tile = crops.growth_stage
        for key,entity in dict(game.entities).items():
            if GameAction in entity and IngameObject in entity:
                if game.net.is_hosting():
                    action = entity[GameAction]
                    if action.action == 'plant':
                        io = entity[IngameObject]
                        game.NewPlant(io.position)
                        action.action = ''
                    if action.action == 'water':
                        health.value = health.value + 3
                        action.action = ''

                        # Get the health component
                        # Add to the health.value when watered

