import os
import sys
import pygame
from screeninfo import get_monitors

monitors = [m for m in get_monitors()]
# Ширина и высота экрана
WIDTH, HEIGHT = monitors[0].width, monitors[0].height - 60
# Переменные игры
SCORE = 0
COEFFICIENT = 1
FPS = 60
ASTEROID_SPAWN_RATE = 50  # Частота появления астероидов
BULLET_SPEED = 10
ASTEROID_SPEED = 2
PLAYER_SPEED = 5

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

skin_index = 0
img_skin_names = ['baseSkin', 'skin2', 'skin3', 'skin4', 'skin5']

# Для авторизации
user_name = None


def load_image(fullname, colorkey=None):
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image
