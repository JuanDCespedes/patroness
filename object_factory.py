from asteroid import Asteroid
from bullet import Bullet
import math

class ObjectFactory:
    def __init__(self, size):
        self.size = size

    def create_asteroid(self):
        return Asteroid(self.size)

    def create_bullet(self, pos, angle, vel):
        return Bullet(pos, angle, vel, self.size)