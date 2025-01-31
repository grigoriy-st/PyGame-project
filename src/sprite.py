import pygame
from settings import WIDTH


class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, start_x, start_y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.left = start_x
        self.rect.top = start_y
        self.speed = 200
        self.moving = True

    def update(self, clock):
        if self.moving:
            elapsed_time = clock.get_time() / 1000.0
            self.rect.x += self.speed * elapsed_time
            # Установка изображение окончания игры посередине
            if self.rect.right >= WIDTH * 0.65:
                self.moving = False
                self.rect.right = WIDTH * 0.65
