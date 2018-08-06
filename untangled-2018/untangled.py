from game.game import GameState
from lib.framework import Framework

"""
Howdy! If you're looking for the game's important code, look in game/game.py :)
"""

if __name__ == "__main__":
    # Make a Framework based on our Game and run it!
    app = Framework(GameState)
    app.main_loop()
