import os
import pygame
from settings import load_image


BULLET_SPEED = 10


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_image('../assets/images/bullet.png')
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        """ Обновление координат пули. """
        self.rect.y -= BULLET_SPEED
        if self.rect.y < 0:
            self.kill()

    def gunshot_sound(self):
        pygame.mixer.init()
        shot_sound = pygame.mixer.Sound('../assets/sounds/gun_sound.wav')
        shot_sound.play()
