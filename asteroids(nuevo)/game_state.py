import pygame
import sys
import random
from pygame.locals import *

class GameState:
    def __init__(self, game_manager):
        self.game_manager = game_manager

    def handle_events(self):
        pass

    def update(self):
        pass

    def render(self):
        pass

class ScoreObserver:
    def update(self, event_type, data):
        if event_type == "collision":
            print(f"Collision detected: {data}")

class PlayingState(GameState):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.observer = ScoreObserver()
        self.game_manager.event_manager.subscribe("collision", self.observer)

    def update(self):
        pygame.event.pump()  # Ensure key states are updated
        self.game_manager.ship.update()
        if random.randint(0, 100) % 25 == 0 and len(self.game_manager.asteroids) < 10:
            asteroid = self.game_manager.factory.create_asteroid()
            asteroid.init_sounds()
            self.game_manager.asteroids.append(asteroid)

        for bullet in self.game_manager.ship.bullets[:]:
            bullet.update()
            if bullet.alcance == 0:
                self.game_manager.ship.bullets.remove(bullet)

        for asteroid in self.game_manager.asteroids[:]:
            asteroid.update()
            for bullet in self.game_manager.ship.bullets[:]:
                if asteroid.rect.colliderect(bullet.rect):
                    self.game_manager.ship.bullets.remove(bullet)
                    self.game_manager.ship.puntos += 1
                    self.game_manager.event_manager.notify("collision", {"type": "bullet_asteroid", "points": 1})
                    asteroid.explotar()
                    self.game_manager.asteroids.remove(asteroid)
                    break
            if self.game_manager.ship.rect.colliderect(asteroid.rect):
                if not self.game_manager.ship.invulnerable:
                    self.game_manager.ship.vida -= 10
                    self.game_manager.ship.invulnerable = True
                    self.game_manager.ship.invulnerable_timer = 120  # 2 seconds at 60fps
                    self.game_manager.event_manager.notify("collision", {"type": "ship_asteroid", "damage": 10})
                    if self.game_manager.ship.vida <= 0:
                        self.game_manager.change_state(GameOverState(self.game_manager))
                asteroid.explotar()
                self.game_manager.asteroids.remove(asteroid)
                break

    def render(self):
        self.game_manager.screen.blit(self.game_manager.background_image, self.game_manager.background_rect)
        fuente = pygame.font.Font(None, 45)
        texto_puntos = fuente.render("Puntos: " + str(self.game_manager.ship.puntos), 1, (250, 250, 250))
        vida_color = (255, 0, 0) if self.game_manager.ship.vida < 30 else (250, 250, 250)
        texto_vida = fuente.render("Vida: " + str(self.game_manager.ship.vida), 1, vida_color)
        self.game_manager.screen.blit(texto_vida, (600, 50))
        self.game_manager.screen.blit(texto_puntos, (100, 50))

        for bullet in self.game_manager.ship.bullets:
            self.game_manager.screen.blit(bullet.image, bullet.rect)
        if self.game_manager.ship.invulnerable:
            # Make ship semi-transparent during invulnerability
            temp_image = self.game_manager.ship.imagen.copy()
            temp_image.set_alpha(128)  # 50% transparency
            self.game_manager.screen.blit(temp_image, self.game_manager.ship.rect)
        else:
            self.game_manager.screen.blit(self.game_manager.ship.imagen, self.game_manager.ship.rect)
        for asteroid in self.game_manager.asteroids:
            self.game_manager.screen.blit(asteroid.image, asteroid.rect)

        pygame.display.update()
        pygame.time.delay(10)

class GameOverState(GameState):
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def render(self):
        self.game_manager.screen.blit(self.game_manager.background_image, self.game_manager.background_rect)
        fuente_go = pygame.font.Font(None, 100)
        texto_fin = fuente_go.render("GAME OVER", 1, (250, 0, 0))
        self.game_manager.screen.blit(texto_fin, (150, 250))
        pygame.display.update()
        pygame.time.delay(10)