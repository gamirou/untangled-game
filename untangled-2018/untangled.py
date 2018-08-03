import sys
import uuid
import pygame

from typing import List

from ecs.menu import MenuState, MenuStates
from ecs.network import Network
from ecs.systems.rendersystem import RenderSystem
from ecs.systems.userinputsystem import UserInputSystem
from ecs.components.component import *


class Framework:
    caption = 'Untangled 2018'
    dimensions = (1024, 1024)
    fps = 60
    running = True
    clock = pygame.time.Clock()

    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption(self.caption)
        self.screen = pygame.display.set_mode(self.dimensions, pygame.HWSURFACE | pygame.DOUBLEBUF)

        self.net = Network()

        self.state = MenuState(self)

    def main_loop(self):
        self.clock.tick()
        while self.running:
            self.screen.fill((0, 0, 0))
            dt = self.clock.tick(self.fps) / 1000.0
            events = [ event for event in pygame.event.get() ]
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                    break
            self.state.update(dt, events)

            pygame.display.update()

        pygame.quit()
        self.net.close()
        sys.exit()

    def enter_game(self):
        self.state = GameState(self)


class GameState:
    entities = {}
    systems = []

    def __init__(self, framework: Framework):
        self.framework = framework
        self.screen = framework.screen
        self.net = framework.net

        self.systems.extend([
            UserInputSystem(),
            RenderSystem(self.screen)
        ])

        if self.net.is_hosting():
            self.on_player_join(self.net.get_id())

    def add_entity(self, components: List[dataclass]) -> uuid.UUID:
        key = uuid.uuid4()
        self.entities[key] = {type(value): value for (value) in components}
        return key

    def on_player_join(self, player_id):
        self.add_entity([
            RenderComponent(x=0, y=0, width=10, height=10, color='white'),
            PlayerControlComponent(player_id=player_id),
        ])

    def on_player_quit(self, player_id):
        pass

    def update(self, dt: float, events) -> None:
        self.net.pull_game(self)

        # update our systems
        for system in self.systems:
            system.update(self, dt, events)

        self.net.push_game(self)

if __name__ == "__main__":
    app = Framework()
    app.main_loop()
