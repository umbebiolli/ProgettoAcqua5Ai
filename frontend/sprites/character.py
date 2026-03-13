import pygame

class Character:
    def __init__(self, image_path, x, y, rect=None):
        self.x = x
        self.y = y
        self.image_full = pygame.image.load(image_path).convert_alpha()
        
        # Se viene passato un 'rect' (rettangolo), ritaglia solo quella faccia!
        if rect:
            self.image = self.image_full.subsurface(rect)
        else:
            self.image = self.image_full

    def draw(self, screen):
        # Disegna il personaggio alle sue coordinate attuali
        screen.blit(self.image, (self.x, self.y))