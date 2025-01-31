import pygame
from bullet import Bullet
from settings import WIDTH, HEIGHT

PLAYER_SPEED = 5
img_skin_names = ['baseSkin', 'skin2', 'skin3', 'skin4', 'skin5']


class Player(pygame.sprite.Sprite):
    def __init__(self, skin_index=0):
        super().__init__()
        # global img_skin_names, skin_index
        self.image = pygame.Surface((70, 70))

        self.skin_index = skin_index
        skin_name = img_skin_names[self.skin_index % len(img_skin_names)]

        self.img = pygame.image.load(f'../assets/images/{skin_name}.png')
        self.img = pygame.transform.scale(self.img, (70, 70))
        self.rect = self.img.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_UP]:
            self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN]:
            self.rect.y += PLAYER_SPEED

        # Ограничение движения игрока по окну
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(HEIGHT - self.rect.height, self.rect.y))

    def shoot(self):
        """ Создание выстрела. """
        bullet = Bullet(self.rect.centerx, self.rect.top)
        bullet.gunshot_sound()
        return bullet

    def draw(self, surface):
        """ Метод для отрисовки игрока на экране. """
        surface.blit(self.img, self.rect.topleft)

    def set_ski_index_up(self):
        self.skin_index += 1

    def set_ski_index_down(self):
        self.skin_index += 1
