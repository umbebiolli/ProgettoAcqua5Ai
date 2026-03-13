import pygame

class BadEnding:
    def __init__(self, manager):
        self.manager = manager
        self.font = pygame.font.SysFont(None, 50)
        self.sub_font = pygame.font.SysFont(None, 30)

    def update(self, events, state):
        for e in events:
            if e.type == pygame.KEYDOWN:
                # Potreste resettare il gioco qui se volete
                pass

    def draw(self, screen, state):
        screen.fill((50, 0, 0)) # Sfondo rosso scuro (guerra)
        
        txt = self.font.render("GUERRA PER L'ACQUA", True, (255, 255, 255))
        reason = self.sub_font.render("La civiltà è crollata prima del 2100.", True, (200, 200, 200))
        
        screen.blit(txt, (250, 200))
        screen.blit(reason, (280, 280))