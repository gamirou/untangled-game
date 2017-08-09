from enum import Enum

import pygame

import map

'''
TileAttribute represents the actions which a tile is able to inflict upon a player.

'''
class TileAttribute(Enum): #I don't actually know how this works, someone else needs to fix it - Nat
    COLLIDE =   0b0001
    SPIKES  =   0b0010 #Make this hurt you but allow you to move through normally
    SWIM    =   0b0011
    SLOW    =   0b0100
    HIDE    =   0b0101

class TileType(Enum):
    GRASS = ([53],  [])
    DIRT = ([2], [])
    BIGTREE1 = ([156], [])
    BIGTREE2 = ([157], [])
    BIGTREE3 = ([172], [])
    BIGTREE4 = ([173], [])
    BUSH = ([137], [ TileAttribute.COLLIDE ])
    TREE = ([145],  [ TileAttribute.COLLIDE ])
    SANDTREE = ([160], [ TileAttribute.HIDE ])
    BLUE_BLOCK = ([177],  [])
    RED_BLOCK = ([129],  [])
    BLUE_SPAWN = ([121],  [])
    RED_SPAWN = ([140], [])
    BRICK = ([7],  [ TileAttribute.COLLIDE ])
    BRIDGE = ([21],  [])
    WATER = ([205,206,207],  [ TileAttribute.SWIM ])
    SHELTER = ([37],  [ TileAttribute.COLLIDE ])
    SAND = ([18],  [ TileAttribute.SLOW ])
    LAVA = ([166, 167, 168, 182, 183, 184, 198, 199, 200, 214, 215, 216, 229, 230, 229, 216, 215, 214, 299, 199, 198, 184, 183, 182, 168, 167],  [ TileAttribute.SPIKES ])
    MELON = ([137], [ TileAttribute.COLLIDE ])

    def __init__(self, tileset_id, attributes):
        self.tileset_id = tileset_id
        self.attributes = attributes
        self.animationFrame = 0
        #for attribute in attributes:
            # bitwise or - combines each binaru number into one number
            # a TileType with WATER and COLLIDE would look like 1001
        #    self.attributes = self.attributes | attribute.value

    def has_attribute(self, attribute):
        # bitwise and - sees if one binaru number contains another
        #return self.attributes & attribute.value == attribute.value
        return attribute in self.attributes

    def get_attributes(self):
        return self.attributes


class Tileset():
    def __init__(self, image, grid_dimensions, render_dimensions=(map.TILE_PIX_WIDTH, map.TILE_PIX_HEIGHT)):
        self.image = pygame.image.load(image)
        self.grid_dimensions = grid_dimensions
        self.render_dimensions = render_dimensions
        self.surfaces = {}

    def get_surface_by_id(self, id):
        if id in self.surfaces:
            return self.surfaces[id]

        clip_x, clip_y = self.find_position(id)

        cur_tile_width = (self.image.get_width() // self.grid_dimensions[0])
        cur_tile_height = (self.image.get_height() // self.grid_dimensions[1])

        clip_rect = (
            cur_tile_width * clip_x,
            cur_tile_height * clip_y,
            cur_tile_width,
            cur_tile_height
        )

        subsurface = self.image.subsurface(clip_rect).convert_alpha()
        subsurface = pygame.transform.scale(subsurface, self.render_dimensions)
        self.surfaces[id] = subsurface

        return self.surfaces[id]

    def find_position(self, id):
        x = id % self.grid_dimensions[0]
        y = id // self.grid_dimensions[1]

        return (x, y)

    def find_id(self, x, y):
        return y * self.grid_dimensions[1] + x
