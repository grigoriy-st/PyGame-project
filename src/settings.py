import os
import sys
import pygame
from screeninfo import get_monitors

monitors = [m for m in get_monitors()]
# Ширина и высота экрана
# WIDTH, HEIGHT = monitors[0].width, monitors[0].height - 60
WIDTH, HEIGHT = 800, 800  # Для удобства тестирования
# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

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

# def settings():
#     ''' отображение видео в настройках '''
#     pygame.init()
#     screen_width = 1000
#     screen_height = 1000
#     # pygame.display.set_caption("Настройки")
#     # None - использовать шрифт по умолчанию, 74 - размер шрифта

#     # font = pygame.font.Font(None, 74)
#     # Текст, антиалиасинг, цвет текста
#     # text = font.render("Добро пожаловать в настройки!",
#                           True, (255, 255, 255))
#     #
#     # text_rect = text.get_rect(center=(screen_width // 2, 0))
#     # text_rect.top = 80
#     pygame.display.flip()
#     screen = pygame.display.set_mode((screen_width, screen_height))

#     # Загрузка видео
#     #video_path = '../assets/images/rotated_video1.mp4'
#     #clip = VideoFileClip(video_path)
#     #frames = [clip.get_frame(t) for t in range(int(clip.duration))]

#     # Основной цикл
#     running = True
#     clock = pygame.time.Clock()
#     frame_index = 0

#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False

#         # Получение текущего кадра
#         # if frame_index < len(frames):
#         #     frame = frames[frame_index]
#         #     frame_surface = pygame.surfarray.make_surface(frame)
#         #     screen.blit(frame_surface, (0, 0))
#         #     frame_index += 1
#         # else:
#         #     frame_index = 0  # Перезапуск видео

#         pygame.display.flip()
#         # clock.tick(60)  # Ограничение FPS

#     pygame.quit()
