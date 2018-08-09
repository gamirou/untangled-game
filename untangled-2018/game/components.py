from typing import List
from typing import Tuple
from typing import Union
from pygame import Rect
import random

from lib.component import component
from lib.framework import Framework
from game.systems.collisionsystem import CollisionCall
from game.systems.particlesystem import Particle

@component(networked=True)
class IngameObject:
    """Gives an entity a place and size in game."""
    position: Tuple[int, int]
    size: Tuple[int, int]
    id = None

@component(networked=True)
class Health:
    """Gives the entity health"""
    value: int

@component(networked=True)
class CanPickUp:
    pickedUp: bool = False
    quantity: int = 1

@component(networked=True)
class WaterBar:
    """Gives the entity a water bar"""
    value: int
    disabled: bool = False

@component(networked=True)
class Inventory:
    """Gives a player items"""
    items: List[Tuple[str, int]]
    maxSlots: int = 6 # it represents the last index, not the number of slots
    activeSlot: int = 0
    hoverSlot: int = None

    itemSlotOffset: int = 6
    slotOffset: int = 10
    slotSize: int = 55

    height: float = slotOffset*2 + slotSize
    width: float = slotSize * maxSlots + (slotOffset+1) * maxSlots * 2

    x: float = Framework.dimensions[0] / 2 - width / 2
    y: float = Framework.dimensions[1] - height - slotOffset

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

directionVelocity = {
    'default':[0,0],
    'left':[-1,0],
    'right':[1,0],
    'up':[0,-1],
    'down':[0,1]
}

@component(networked=True)
class Directioned:
    """States that an entity will be pointing in a certain direction.
    e.g. if walking"""
    direction: str = 'default'

    def toVelocity(self):
        return directionVelocity[self.direction]


@component(networked=True)
class Profile:
    """Gives an entity a name and gender."""
    name: str = 'Player'
    gender: str = 'Unknown'

@component(networked=True)
class PlayerControl:
    """Lets an entity be controlled by specific player's arrow keys."""
    player_id: str

@component(networked=True)
class ParticleEmitter:
    # square / circle / ring / star
    # blank means random 
    particleTypes: list
    # offset from IngameObject
    offset: Tuple[int,int] = (0,0)
    # Initial movement
    velocity: Tuple[float,float] = (0.0,0.0)
    # Added to velocity each frame
    acceleration: Tuple[float,float] = (0.0,0.0)
    colour: Tuple[int,int,int] = (255,255,255)
    # "above" or "below" the object it's on render
    height: str = "below"
    randomness: Tuple[float,float] = (1.0,1.0)
    lifespan: int = 10
    doCreateParticles: bool = True
    # Will multiply velocity by the directionVelocity dict above
    # 0 - ignore direction
    # 1 - times by direction
    # 2 - times by inverse direction (so particles go in opposite to facing)
    directionMode: int = 0
    onlyWhenMoving: bool = False

    #DO NOT USE THIS MANUALLY
    _prePosition = (0,0)

    def getParticle(self,entity):
        if self.doCreateParticles and IngameObject in entity:
            doParticles = True
            if self.onlyWhenMoving:
                if self._prePosition == entity[IngameObject].position:
                    doParticles = False
                else:
                    self._prePosition = entity[IngameObject].position

            if doParticles:
                l = ["square","circle","ring","star"]
                if len(self.particleTypes) > 0:
                    l = self.particleTypes
                t = random.choice(l)
                pos = (entity[IngameObject].position[0] + self.offset[0], entity[IngameObject].position[1] + self.offset[1])
                vel = self.velocity
                if self.directionMode > 0 and Directioned in entity:
                    dire = entity[Directioned].toVelocity()
                    modi = 1
                    if self.directionMode == 2:
                        modi = -1
                    vel = (vel[0] * dire[0] * modi, vel[1] * dire[1] * modi)
                part = Particle(
                    t,
                    pos,
                    self.lifespan,
                    velocity = vel,
                    acceleration = self.acceleration,
                    colour = self.colour,
                    below = (self.height == "below"),
                    randomness = self.randomness
                )
                return part
        return None

        

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
