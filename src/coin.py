import pygame
import random
from settings import WIDTH, HEIGHT, load_image


COIN_SPAWN_RATE = 100  # Частота появления астероидов


class Coin(pygame.sprite.Sprite):
    def __init__(self, coin_speed=2, coefficient=1):
        super().__init__()
        self.image = load_image('../assets/images/coin.png')
        self.image = pygame.transform.scale(self.image,
                                            (30, 39))
        self.coin_speed = coin_speed
        self.coefficient = coefficient
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), 0))

    def update(self):
        """ Обновление координат монеты. """
        self.rect.y += self.coin_speed
        if self.rect.y > HEIGHT:
            self.kill()

    def increase_speed(self):
        """ Увеличение скорости движения. """
        self.coin_speed *= self.coefficient + 1
        self.coefficient += 1
    
    def sound_of_collecting_coin(self):
        """ Звук сбора монеты. """
        shot_sound = pygame.mixer.Sound(
            '../assets/sounds/coin_sound.wav')
        shot_sound.play()