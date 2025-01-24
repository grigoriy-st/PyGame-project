import os
import pygame
import sys
import random
# Константы
WIDTH, HEIGHT = 1000, 1000  # Ширина и высота окна
FPS = 60
ASTEROID_SPAWN_RATE = 25  # Частота появления астероидов
BULLET_SPEED = 10
ASTEROID_SPEED = 3
PLAYER_SPEED = 5

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

skin_index = 0
img_skin_names = ['baseSkin', 'skin2', 'skin3', 'skin4', 'skin5']

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
        # skin_name = img_skin_names[ skin_index % (len(img_skin_names)) ]
        # self.img = pygame.image.load(f'assets/images/{skin_name}.png')
        # self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        skin_name = img_skin_names[skin_index % len(img_skin_names)]
        self.img = pygame.image.load(f'assets/images/{skin_name}.png')
        self.img = pygame.transform.scale(self.img, (70, 70))  # Измените размер изображения, если необходимо
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
        return bullet

    def draw(self, surface):
        """ Метод для отрисовки игрока на экране. """
        surface.blit(self.img, self.rect.topleft)

class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        if random.randint(0,  2) == 1:
            self.image = load_image('assets/images/meteorit2.png')
        else:
            self.image = load_image('assets/images/meteorit.png')
        self.image = pygame.transform.scale(self.image, (40, 40))
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
        skin_index = 0
        
        while True:
            self.screen.fill((0, 0, 0))
            
            # Главный текст
            welcome_text = self.font.render("Добро пожаловать в космическую бурю!", True, (255, 255, 255))
            text_rect = welcome_text.get_rect(center=(WIDTH // 2, 60 ))
            self.screen.blit(welcome_text, text_rect)

            # Кнопка настройки
            settings_btn = pygame.image.load('assets/images/settings.png')
            settings_btn = pygame.transform.scale(settings_btn, (60, 60))
            settings_btn_rect = settings_btn.get_rect()
            settings_btn_rect.topleft = (30, 30)
            self.screen.blit(settings_btn, (30, 30))

            # Кнопка для начала игры
            button_text = self.button_font.render("Начать игру", True, (255, 255, 255))
            button_rect = button_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 250))
            pygame.draw.rect(self.screen, (0, 128, 0), button_rect.inflate(20, 20))  # Кнопка
            self.screen.blit(button_text, button_rect)

            # Кнопка слева
            left_arrow = pygame.image.load('assets/images/arrow.png')
            left_arrow = pygame.transform.scale(left_arrow, (200, 200))
            l_arrow_rect = left_arrow.get_rect()
            l_arrow_rect.topleft = (100, 300)
            self.screen.blit(left_arrow, (100, 300))

            # Кнопка справа
            right_arrow = pygame.image.load('assets/images/arrow.png')
            right_arrow = pygame.transform.scale(right_arrow, (200, 200))
            right_arrow = pygame.transform.flip(right_arrow, True, False)
            r_arrow_rect = right_arrow.get_rect()
            r_arrow_rect.topleft = (650, 300)
            self.screen.blit(right_arrow, (650, 300))

            # Скин на выбор
            skin_name = img_skin_names[ skin_index % (len(img_skin_names)) ]
            skin_img = pygame.image.load(f'assets/images/{skin_name}.png')
            skin_img = pygame.transform.scale(skin_img, (300, 300))
            self.screen.blit(skin_img, (350, 250))

            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        return

                    # Выборка скина космолёта
                    if l_arrow_rect.collidepoint(event.pos):
                        skin_index -= 1

                    if r_arrow_rect.collidepoint(event.pos):
                        skin_index += 1

                    if settings_btn_rect.collidepoint(event.pos):
                        print("Ты кликнул по настройкам")

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return

                
            pygame.display.flip()

    def show_game_over_screen(self):
        """ Отображение конца игры. """
        pygame.display.set_caption("Game over")
        blue = (0, 0, 255)

        try:
            image = pygame.image.load('assets/images/gameover.png')

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
            player.draw(self.screen)

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
