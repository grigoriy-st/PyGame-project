import pygame
import random
from PIL import Image


def extract_frames(gif_path, width=30, height=30):
    """ Выборка фреймов. """
    img = Image.open(gif_path)
    frames = []
    try:
        while True:
            frame = img.copy()
            if width and height:
                # Изменяем размер кадра
                frame = frame.resize((width, height), Image.LANCZOS)
            frames.append(frame)
            img.seek(img.tell() + 1)
    except EOFError:
        pass
    return frames


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, gif_path, width=None, height=None):
        super().__init__()
        self.frames = extract_frames(gif_path, width, height)
        # Преобразуем кадры из Pillow в Pygame
        self.frames = [pygame.image.fromstring(
            frame.tobytes(), frame.size, frame.mode).convert_alpha()
            for frame in self.frames]
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(center=(x, y))
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100  # Время между кадрами в миллисекундах
        self.angle = random.randint(0, 360)

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame += 1
            if self.current_frame >= len(self.frames):
                self.kill()  # Удаляем взрыв после завершения анимации
            else:
                self.image = self.frames[self.current_frame]
                # Вращаем изображение
                self.image = pygame.transform.rotate(self.image, self.angle)
                self.rect = self.image.get_rect(center=self.rect.center)
