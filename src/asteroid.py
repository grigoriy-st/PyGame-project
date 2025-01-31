import pygame
import random
from settings import WIDTH, HEIGHT, load_image


ASTEROID_SPAWN_RATE = 50  # Частота появления астероидов


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, asteroid_speed=2, coefficient=1):
        super().__init__()
        if random.randint(0,  2) == 1:
            self.image = load_image('../assets/images/meteorit2.png')
        else:
            self.image = load_image('../assets/images/meteorit.png')
        random_size = random.randint(30, 130)
        self.image = pygame.transform.scale(self.image,
                                            (random_size, random_size))
        self.asteroid_speed = asteroid_speed
        self.coefficient = coefficient
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), 0))

    def update(self):
        """ Обновление координат астероида. """
        self.rect.y += self.asteroid_speed
        if self.rect.y > HEIGHT:
            self.kill()

    def increase_speed(self):
        """ Увеличение скорости движения. """
        self.asteroid_speed *= self.coefficient + 1
        self.coefficient += 1
