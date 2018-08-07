from typing import List
from typing import Tuple
from typing import Union

from lib.component import component
from lib.framework import Framework

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
    default: List[int]
    left: Union[List[int], None]
    right: Union[List[int], None]
    up: Union[List[int], None]
    down: Union[List[int], None]
    moving: bool = False

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
