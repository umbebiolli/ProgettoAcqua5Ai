import pygame

class WaterBar:

    def __init__(self,x,y):

        self.x = x
        self.y = y

    def draw(self,screen,value):

        width = 200
        height = 20

        ratio = value / 100
        fill = width * ratio

        pygame.draw.rect(screen,(255,255,255),(self.x,self.y,width,height),2)
        pygame.draw.rect(screen,(0,120,255),(self.x,self.y,fill,height))