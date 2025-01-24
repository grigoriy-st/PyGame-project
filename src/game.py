import os
import pygame
import sys
import random
# Константы
WIDTH, HEIGHT = 800, 600  # Ширина и высота окна
FPS = 60
ASTEROID_SPAWN_RATE = 25  # Частота появления астероидов
BULLET_SPEED = 10
ASTEROID_SPEED = 3
PLAYER_SPEED = 5

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

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
            if self.rect.right >= WIDTH * 0.85:  # Установка изображение окончания игры посередине
                self.moving = False
                self.rect.right = WIDTH * 0.85


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 30))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

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
        return bullet


class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), 0))

    def update(self):
        """ Обновление координат астероида. """
        self.rect.y += ASTEROID_SPEED
        if self.rect.y > HEIGHT:
            self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        """ Обновление координат пули. """
        self.rect.y -= BULLET_SPEED
        if self.rect.y < 0:
            self.kill()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Космическая буря")
        self.running = True
        self.font = pygame.font.Font(None, 50)
        self.button_font = pygame.font.Font(None, 48)

    def show_welcome_screen(self):
        """ Отображение приветственного окна. """
        while True:
            self.screen.fill((0, 0, 0))

            # Главный текст
            welcome_text = self.font.render("Добро пожаловать в космическую бурю!", True, (255, 255, 255))
            text_rect = welcome_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
            self.screen.blit(welcome_text, text_rect)

            # Кнопка для начала игры
            button_text = self.button_font.render("Начать игру", True, (255, 255, 255))
            button_rect = button_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
            pygame.draw.rect(self.screen, (0, 128, 0), button_rect.inflate(20, 20))  # Кнопка
            self.screen.blit(button_text, button_rect)

            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return

            pygame.display.flip()

    def show_game_over_screen(self):
        """ Отображение конца игры. """
        pygame.display.set_caption("Game over")
        blue = (0, 0, 255)
               
        try:
            image = pygame.image.load('../assets/images/gameover.png')

        except pygame.error as e:
            print(f"Ошибка загрузки изображения: {e}")
            pygame.quit()
            exit()

        image = image.convert_alpha()

        image_sprite = Sprite(
            image,
            -image.get_rect().width,
            HEIGHT // 2 - image.get_rect().height // 2,
        )
        all_sprites = pygame.sprite.Group()
        all_sprites.add(image_sprite)
        clock = pygame.time.Clock()

        while self.running:
            self.screen.fill(blue)

            button_text = self.button_font.render("Начать новую игру", True, (255, 255, 255))
            button_rect = button_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 200))
            pygame.draw.rect(self.screen, (0, 128, 0), button_rect.inflate(20, 20))  # Кнопка
            self.screen.blit(button_text, button_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        self.show_welcome_screen()
                        self.main_game()  # начало новой игры
                        break

                        return
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.show_welcome_screen()
                            self.main_game()  # начало новой игры
                            break

                            return
 
            all_sprites.update(clock)
            # self.screen.fill(blue)
            all_sprites.draw(self.screen)
            pygame.display.flip()
            clock.tick(60)
        pygame.quit()

    def run(self):
        self.show_welcome_screen()
        self.main_game()

    def main_game(self):
        """ Основной игровой цикл. """
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        clock = pygame.time.Clock()

        # Группы спрайтов
        all_sprites = pygame.sprite.Group()
        asteroids = pygame.sprite.Group()
        bullets = pygame.sprite.Group()

        # Создание игрока
        player = Player()
        all_sprites.add(player)

        # Основной игровой цикл
        score = 0

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        print("bullet")
                        bullet = player.shoot()  # Выстрел
                        all_sprites.add(bullet)
                        bullets.add(bullet)
                    
            if random.randint(1, ASTEROID_SPAWN_RATE) == 1:
                asteroid = Asteroid()
                all_sprites.add(asteroid)
                asteroids.add(asteroid)

            # Обновление спрайтов
            all_sprites.update()

            # Проверка на столкновения
            for bullet in bullets:
                hit_asteroids = pygame.sprite.spritecollide(bullet, asteroids, True)
                if hit_asteroids:
                    bullet.kill()
                    score += len(hit_asteroids)

            # Проверка на столкновение игрока с астероидами
            if pygame.sprite.spritecollideany(player, asteroids):
                self.show_game_over_screen()

            # Отрисовка
            self.screen.fill(BLACK)
            all_sprites.draw(self.screen)

            # Отображение счета
            font = pygame.font.Font(None, 36)
            text = font.render(f'Score: {score}', True, WHITE)
            self.screen.blit(text, (10, 10))

            pygame.display.flip()
            clock.tick(FPS)


        self.running = False
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
