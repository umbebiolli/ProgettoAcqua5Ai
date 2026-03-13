import pygame
import sys

from scene_manager import SceneManager
from game_state import GameState
from settings import *

pygame.init()

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Water Conflict Simulation")

clock = pygame.time.Clock()

manager = SceneManager()
state = GameState()

while True:

    events = pygame.event.get()

    for event in events:

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    manager.update(events,state)

    screen.fill((30,30,40))

    manager.draw(screen,state)

    pygame.display.flip()

    clock.tick(FPS)