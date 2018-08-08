from typing import List
from typing import Tuple
from typing import Union
import time
from lib.component import component

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
class Crops:
    """Stores infomation about crops"""
    name: str
    growth_rate: int
    dehydration_rate: int
    growth_stage:int
    max_growth_stage:int
    plantage_time:float = time.time()
@component(networked=True)
class SpriteSheet:
    """Gives an entity an image and animations."""
    path: str
    tile_size: int
    tiles: dict
    default_tile: int = 0
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
@component(networked=True)
class GameAction:
    action: str = ''
