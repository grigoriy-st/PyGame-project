import pygame
import random
from settings import WIDTH, ASTEROID_SPEED, HEIGHT, load_image


class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        if random.randint(0,  2) == 1:
            self.image = load_image('../assets/images/meteorit2.png')
        else:
            self.image = load_image('../assets/images/meteorit.png')
        random_size = random.randint(30, 130)
        self.image = pygame.transform.scale(self.image,
                                            (random_size, random_size))
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), 0))

    def update(self):
        """ Обновление координат астероида. """
        self.rect.y += ASTEROID_SPEED
        if self.rect.y > HEIGHT:
            self.kill()
