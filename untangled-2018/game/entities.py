from game.components import *
from game.systems.collisionsystem import CollisionCall

def create_player(player_id):
    return [
        # They should have a position and size in game
        IngameObject(position=(0, 0), size=(64, 64)),

        # They should have a health
        Health(value=100),

        # They should have an inventory
        Inventory([]),

        # They should be facing a certain direction
        Directioned(direction='default'),
        WaterBar(value=100),

        # They will have a name and gender
        Profile(),

        # We know what they may look like
        SpriteSheet(
            path='./assets/sprites/player.png',
            tile_size=48,
            moving=False,
            tiles={
                'default':[58],
                'left':[70,71,69],
                'right':[82,83,81],
                'up':[94,95,93],
                'down':[58,59,57]
            }
        ),

        # The player who has connected con control them with the arrow keys
        PlayerControl(player_id=player_id),

        Collidable(
            call = CollisionCall()
        ),

        ParticleEmitter(
            particleTypes = ["ring","star"],
            offset = (0,32),
            velocity = (1,1),
            directionMode = 2,
            colour = (137, 63, 69),
            onlyWhenMoving = True,
            randomness = (3,3)
        )
    ]

def create_background_music():
    return [
        BackgroundMusic (
            path="assets/sounds/overworld.wav"
        )
    ]

def create_test_collision_object():
    return [
        IngameObject(position=(0,0), size=(128,128)),
        SpriteSheet(
            path='./assets/sprites/test.png',
            tile_size=8,
            moving=False,
            tiles={
                'default':[0]
            }
        ),
        Collidable(
            call = CollisionCall()
        )
    ]

def create_test_item_object(animated=False):
    if animated:
        return [
            IngameObject(position=(200,100), size=(49,49)),
            SpriteSheet(
                path='./assets/sprites/BOUNCE_enemy.png',
                tile_size=32,
                tiles={
                    'default': [3, 4, 5],
                },
                moving=True
            ),
            Collidable(
                call = CollisionCall()
            ),
            # Every item has this component
            CanPickUp(quantity=1),
            Directioned(direction='default')
        ]
    else:
        return [
            IngameObject(position=(100,100), size=(49,49)),
            SpriteSheet(
                path='./assets/sprites/test.png',
                tile_size=8,
                moving=False,
                tiles={
                    'default':[0]
                }
            ),
            Collidable(
                call = CollisionCall()
            ),
            # Every item has this component
            CanPickUp(quantity=2)
        ]
