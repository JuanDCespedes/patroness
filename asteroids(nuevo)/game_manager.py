import pygame
import sys
from pygame.locals import *
import random
from ship import Ship
from asteroid import Asteroid
from bullet import Bullet
from object_factory import ObjectFactory
from event_manager import EventManager
from game_state import GameState, PlayingState, GameOverState

class GameManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(GameManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, size=(800, 600)):
        if not hasattr(self, 'initialized'):
            self.size = size
            self.factory = ObjectFactory(self.size)
            self.asteroids = []
            self.event_manager = EventManager()
            self.state = PlayingState(self)
            self.initialized = True

    def run(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode(self.size)
        self.background_image = pygame.image.load("imagenes/space.png")
        self.background_rect = self.background_image.get_rect()
        self.ship = Ship(self.size, self.factory)
        self.ship.init_sounds()
        pygame.mixer.music.load("sonido/outer.mp3")
        pygame.mixer.music.play(1)
        pygame.display.set_caption("Asteroids")

        while True:
            self.state.handle_events()
            self.state.update()
            self.state.render()

    def change_state(self, state):
        self.state = state