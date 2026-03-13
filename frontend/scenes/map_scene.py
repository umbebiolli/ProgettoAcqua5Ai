import pygame
from ui.water_bar import WaterBar
from sprites.character import Character
from settings import *

# Assicurati di avere questo file creato, o adatta il nome
from scenes.good_ending_scene import GoodEnding 

class MapScene:
    def __init__(self, manager):
        self.manager = manager
        
        self.map = pygame.image.load("assets/map.png")
        self.barA = WaterBar(50, 50)
        self.barB = WaterBar(750, 50)
        
        self.timer = 0
        self.font = pygame.font.SysFont(None, 30)

        from ui.button import Button
        
        # Bottoni Scelta Iniziale
        self.buttonA = Button("Paese A perde acqua", 300, 250, 200, 50)
        self.buttonB = Button("Paese B perde acqua", 550, 250, 200, 50)
        
        # Bottoni Scelta Finale (Collaborazione o Guerra)
        self.btn_collab = Button("Collaborazione", 250, 300, 200, 50)
        self.btn_guerra = Button("Guerra", 550, 300, 200, 50)

        # Gestore delle fasi: "scelta_iniziale", "simulazione", "camminata", "domanda", "collaborazione"
        self.fase_gioco = "scelta_iniziale" 
        self.losing_village = None

        # RITAGLIO PERSONAGGI (x, y, larghezza, altezza). 
        # Modifica 150, 150 se i volti sono più grandi o più piccoli
        self.char_walker = None # Lo creiamo dopo in base a chi perde acqua
        
        self.characters = [
            # Primo volto in alto a sinistra (0, 0)
            Character("assets/villageA_chars.png", 150, 400, rect=pygame.Rect(0, 0, 150, 150)),
            # Secondo volto (150, 0)
            Character("assets/villageA_chars.png", 220, 400, rect=pygame.Rect(150, 0, 150, 150)), 
        ]

    def update(self, events, state):

        # FASE 1: Scelta di chi perde acqua
        if self.fase_gioco == "scelta_iniziale":
            for e in events:
                if self.buttonA.clicked(e):
                    self.losing_village = "A"
                    self.char_walker = Character("assets/villageA_chars.png", 150, 400, rect=pygame.Rect(0, 0, 150, 150))
                    self.fase_gioco = "simulazione"
                    
                if self.buttonB.clicked(e):
                    self.losing_village = "B"
                    self.char_walker = Character("assets/villageB_chars.png", 850, 400, rect=pygame.Rect(0, 0, 150, 150))
                    self.fase_gioco = "simulazione"
            return

        # FASE 2: Simulazione anni normale
        elif self.fase_gioco == "simulazione":
            self.timer += 1
            if self.timer > 300:
                state.year += 5
                self.timer = 0

                if self.losing_village == "A": state.water_a -= 10
                if self.losing_village == "B": state.water_b -= 10

            # Evento diga
            if state.year >= 2040 and not getattr(state, 'dam_built', False):
                state.dam_built = True
                if self.losing_village == "B": state.water_b -= 40
                if self.losing_village == "A": state.water_a -= 40

            # Controllo soglia critica dinamico (controlla il villaggio che sta perdendo acqua)
            acqua_attuale = state.water_a if self.losing_village == "A" else state.water_b
            if acqua_attuale < WATER_THRESHOLD:
                self.fase_gioco = "camminata"

        # FASE 3: Il personaggio cammina verso il centro
        elif self.fase_gioco == "camminata":
            # Muovi verso x=500
            if self.char_walker.x < 500: self.char_walker.x += 2
            elif self.char_walker.x > 500: self.char_walker.x -= 2
            
            # Quando arriva al centro esatto (o quasi)
            if abs(self.char_walker.x - 500) <= 2:
                self.fase_gioco = "domanda"

        # FASE 4: Domanda a schermo "Guerra o Collaborazione?"
        elif self.fase_gioco == "domanda":
            for e in events:
                if self.btn_collab.clicked(e):
                    self.fase_gioco = "collaborazione"
                
                if self.btn_guerra.clicked(e):
                    # --- LOGICA GUERRA ---
                    if self.losing_village == "B":
                        # Il villaggio B attacca A per prendersi l'acqua
                        state.water_a = 0 
                    else:
                        # Il villaggio A attacca B
                        state.water_b = 0
                    
                    self.fase_gioco = "conflitto"
                    self.timer = 0

        # FASE 6: Conflitto (mostra il disastro prima del game over)
        elif self.fase_gioco == "conflitto":
            self.timer += 1
            # Facciamo tremare lo schermo o aspettiamo un momento
            if self.timer > 100:
                from scenes.bad_ending_scene import BadEnding
                self.manager.change(BadEnding(self.manager))

        # FASE 5: Collaborazione (Gli anni volano, l'acqua si equalizza)
        elif self.fase_gioco == "collaborazione":
            self.timer += 1
            if self.timer > 50: # Scorre molto più veloce!
                self.timer = 0
                if state.year < 2100:
                    state.year += 1
                    
                    # Calcola la media e avvicina le due barre
                    media = (state.water_a + state.water_b) / 2
                    
                    if state.water_a < media: state.water_a += 1
                    elif state.water_a > media: state.water_a -= 1
                    
                    if state.water_b < media: state.water_b += 1
                    elif state.water_b > media: state.water_b -= 1
                else:
                    # Raggiunto il 2100, si vince!
                    self.manager.change(GoodEnding(self.manager))


    def draw(self, screen, state):
        
        # Disegno Schermata di Scelta Iniziale
        if self.fase_gioco == "scelta_iniziale":
            screen.fill((30, 30, 40))
            text = self.font.render("Quale villaggio perderà acqua?", True, (255, 255, 255))
            screen.blit(text, (330, 200))
            self.buttonA.draw(screen)
            self.buttonB.draw(screen)
            return

        # Disegno Mappa Normale (per tutte le altre fasi)
        screen.blit(self.map, (0, 0))
        self.barA.draw(screen, state.water_a)
        self.barB.draw(screen, state.water_b)

        year_text = self.font.render(f"Year: {state.year}", True, (255, 255, 255))
        screen.blit(year_text, (450, 20))

        # Disegno Personaggi Statici
        for c in self.characters:
            c.draw(screen)

        # Disegno Personaggio in cammino (se serve)
        if self.fase_gioco in ["camminata", "domanda", "collaborazione"]:
            self.char_walker.draw(screen)

        # Disegno Bottoni Domanda Finale
        if self.fase_gioco == "domanda":
            q_text = self.font.render("L'acqua sta finendo! Cosa volete fare?", True, (255, 255, 255))
            screen.blit(q_text, (320, 200))
            self.btn_collab.draw(screen)
            self.btn_guerra.draw(screen)


        # Se c'è guerra, coloriamo lo schermo di rosso trasparente
        if self.fase_gioco == "conflitto":
            overlay = pygame.Surface((1000, 600)) # Dimensioni tua finestra
            overlay.set_alpha(128) # Trasparenza
            overlay.fill((255, 0, 0)) # Rosso
            screen.blit(overlay, (0,0))