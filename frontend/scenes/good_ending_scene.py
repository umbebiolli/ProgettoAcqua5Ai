import pygame

class GoodEnding:

    def __init__(self,manager):

        self.manager = manager
        self.font = pygame.font.SysFont(None,50)

    def update(self,events,state):
        pass

    def draw(self,screen,state):

        text = self.font.render(
        "Cooperazione! I villaggi raggiungono il 2100",True,(255,255,255))

        screen.blit(text,(150,250))