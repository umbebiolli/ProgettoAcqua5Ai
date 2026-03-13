import pygame

class Button:

    def __init__(self,text,x,y,w,h):

        self.rect = pygame.Rect(x,y,w,h)
        self.text = text
        self.font = pygame.font.SysFont(None,30)

    def draw(self,screen):

        pygame.draw.rect(screen,(200,200,200),self.rect)

        txt = self.font.render(self.text,True,(0,0,0))
        screen.blit(txt,(self.rect.x+10,self.rect.y+10))

    def clicked(self,event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True