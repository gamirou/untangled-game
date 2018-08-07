from typing import List
from typing import Tuple
from typing import Union
from pygame import Rect

from lib.component import component
from game.systems.collisionsystem import CollisionCall

@component(networked=True)
class IngameObject:
    """Gives an entity a place and size in game."""
    position: Tuple[int, int]
    size: Tuple[int, int]

@component(networked=True)
class Health:
    """Gives the entity health"""
    value: int

@component(networked=True)
class SpriteSheet:
    """Gives an entity an image and animations."""
    path: str
    tile_size: int
    tiles: dict
    moving: bool = False

@component(networked=True)
class BackgroundMusic:
    path: str

@component(networked=True)
class Directioned:
    """States that an entity will be pointing in a certain direction.
    e.g. if walking"""
    direction: str = 'default'

@component(networked=True)
class Profile:
    """Gives an entity a name and gender."""
    name: str = 'Player'
    gender: str = 'Unknown'

@component(networked=True)
class PlayerControl:
    """Lets an entity be controlled by specific player's arrow keys."""
    player_id: str

@component(networked=False)
class Collidable:
    """Lets an entity collide with another collidable"""
    call: CollisionCall
    canCollide: bool = True
    #rect to override
    customCollisionBox = None
    def setCustomCollisionBox(self, obj: IngameObject, width: int, height: int):
        center = (obj.position[0] + (obj.size[0] / 2), obj.position[1] + (obj.size[1] / 2))
        newTopLeft = (center[0] - (width/2), center[1] - (height/2))
        self.customCollisionBox = Rect(newTopLeft[0], newTopLeft[1], width, height)

    def toRect(self,entity):
        if self.customCollisionBox is not None:
            return self.customCollisionBox
        pos = entity[IngameObject].position
        size = entity[IngameObject].size
        return Rect(
            pos[0] - (size[0] / 2),
            pos[1] - (size[1] / 2),
            entity[IngameObject].size[0],
            entity[IngameObject].size[1]
        )
