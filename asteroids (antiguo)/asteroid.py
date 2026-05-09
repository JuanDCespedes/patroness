import pygame, random, math
from pygame.sprite import Sprite
from pygame.locals import *
class Asteroid(Sprite):
    def __init__(self, cont):
        Sprite.__init__(self)
        self.vel=[random.randint(-2, 2), random.randint (-2,2)]
        self.contenedor=cont
        self.angulo=0
        self.rotacion=random.randint(-20,20)
        self.base_image=pygame.image.load("imagenes/asteroid.png")
        self.image=self.base_image
        self.rect=self.image.get_rect()
        self.rect.move_ip(random.randint(0,self.contenedor[0]), random. randint(0, self.contenedor[1]))
        self.explosion=pygame.mixer.Sound("sonido/explosion.mp3")
        self.explosion.set_volume(0.05)
    def update(self):
        self.angulo+=self.rotacion
        centerx=self.rect.centerx
        centery=self.rect.centery
        self.image=pygame.transform.rotate(self.base_image,self.angulo)
        self.rect=self.image.get_rect()
        self.rect.centerx=centerx
        self.rect.centery=centery
        self.rect=self.rect.move(self.vel)
        self.rect.x=self.rect.x%self.contenedor[0]
        self.rect.y=self.rect.y%self.contenedor[1]
    def explotar(self):
        self.image=pygame.image.load("imagenes/explosion.png")
        self.explosion.play()