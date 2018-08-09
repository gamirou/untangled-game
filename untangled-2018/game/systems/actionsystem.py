import pygame.locals

from lib.system import System
from game.components import *

class ActionSystem(System):
    """This system updates entities based on the actions from the GameAction component"""
    def update(self, game, dt: float, events):
        for key, entity in game.entities.items():
            if GameAction in entity:
                action = entity[GameAction].action

                if action == "drop":
                    if Inventory in entity and Directioned in entity:
                        game.inventorySystem.itemDroppedOff(game, entity, entity[Directioned].direction)