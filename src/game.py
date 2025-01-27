import os
import pygame
import sys
import random
from moviepy import VideoFileClip
from screeninfo import get_monitors

os.chdir("src")

monitors = [m for m in get_monitors()]

# Константы
WIDTH, HEIGHT = monitors[0].width, monitors[0].height - 60  # Ширина и высота окна
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


def settings():
    ''' отображение видео в настройках '''
    pygame.init()
    screen_width = 1000
    screen_height = 1000
    # pygame.display.set_caption("Настройки")
    # font = pygame.font.Font(None, 74)  # None - использовать шрифт по умолчанию, 74 - размер шрифта
    # text = font.render("Добро пожаловать в настройки!", True, (255, 255, 255))  # Текст, антиалиасинг, цвет текста
    #
    # text_rect = text.get_rect(center=(screen_width // 2, 0))
    # text_rect.top = 80
    pygame.display.flip()
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Загрузка видео
    #video_path = '../assets/images/rotated_video1.mp4'
    #clip = VideoFileClip(video_path)
    #frames = [clip.get_frame(t) for t in range(int(clip.duration))]

    # Основной цикл
    running = True
    clock = pygame.time.Clock()
    frame_index = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Получение текущего кадра
        # if frame_index < len(frames):
        #     frame = frames[frame_index]
        #     frame_surface = pygame.surfarray.make_surface(frame)
        #     screen.blit(frame_surface, (0, 0))
        #     frame_index += 1
        # else:
        #     frame_index = 0  # Перезапуск видео

        pygame.display.flip()
        # clock.tick(60)  # Ограничение FPS

    pygame.quit()


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
            if self.rect.right >= WIDTH * 0.65:  # Установка изображение окончания игры посередине
                self.moving = False
                self.rect.right = WIDTH * 0.65


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        global skin_index, img_skin_names
        self.image = pygame.Surface((70, 70))

        skin_name = img_skin_names[skin_index % len(img_skin_names)]

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
        return bullet

    def draw(self, surface):
        """ Метод для отрисовки игрока на экране. """
        surface.blit(self.img, self.rect.topleft)


class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        if random.randint(0,  2) == 1:
            self.image = load_image('../assets/images/meteorit2.png')
        else:
            self.image = load_image('../assets/images/meteorit.png')
        random_size = random.randint(30, 130)
        self.image = pygame.transform.scale(self.image, (random_size, random_size))
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), 0))

    def update(self):
        """ Обновление координат астероида. """
        self.rect.y += ASTEROID_SPEED
        if self.rect.y > HEIGHT:
            self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_image('../assets/images/bullet.png')
        self.image = pygame.transform.scale(self.image, (20, 20))
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

    def show_auth_screen(self):
        global user_name
        self.screen.fill(BLACK)

        clock = pygame.time.Clock() 
        base_font = pygame.font.Font(None, 32) 
        user_text = ''

        input_width = 200
        input_height = 32
        # input_rect = pygame.Rect((WIDTH // 2) - (input_width // 2), (HEIGHT // 2) - (input_height // 2), input_width, input_height) 
        input_rect = pygame.Rect((WIDTH // 2 - 50), (HEIGHT // 2), input_width, input_height)

        color_active = pygame.Color('lightskyblue3') 
        color_passive = pygame.Color('chartreuse4') 
        color = color_passive 
        active = False
        
        button_text = self.button_font.render("Войти", True, (255, 255, 255))
        button_rect = button_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 200))
        pygame.draw.rect(self.screen, (0, 128, 0), button_rect.inflate(20, 20))  # Кнопка
        
        welcome_text = self.font.render("Добро пожаловать в космическую бурю!", True, (255, 255, 255))
        text_rect = welcome_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200))

        text2= self.font.render("Введите своё имя:", True, (255, 255, 255))
        text2_rect = welcome_text.get_rect(center=(WIDTH // 2 + 200, HEIGHT // 2 - 30))

        while True: 
            for event in pygame.event.get(): 
        
                if event.type == pygame.QUIT: 
                    pygame.quit() 
                    sys.exit() 
        
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    if input_rect.collidepoint(event.pos): 
                        active = True
                    else: 
                        active = False

                    if button_rect.collidepoint(event.pos):
                        user_name = user_text
                        return

                if event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_BACKSPACE: 
                        user_text = user_text[:-1] 
                    else: 
                        user_text += event.unicode
                    
                    
            
                    
            self.screen.fill(BLACK)
            self.screen.blit(button_text, button_rect)
            self.screen.blit(welcome_text, text_rect)
            self.screen.blit(text2, text2_rect)

            if active: 
                color = color_active 
            else: 
                color = color_passive 
            
            pygame.draw.rect(self.screen, color, input_rect) 
            text_surface = base_font.render(user_text, True, (255, 255, 255)) 
            self.screen.blit(text_surface, (input_rect.x+5, input_rect.y+5)) 
            input_rect.w = max(100, text_surface.get_width()+10) 
            pygame.display.flip() 
            # 60 frames should be passed. 
            clock.tick(60) 

    def show_welcome_screen(self):
        """ Отображение приветственного окна. """
        global skin_index
        while True:
            self.screen.fill((0, 0, 0))
            
            # Главный текст
            welcome_text = self.font.render(f"{user_name}, добро пожаловать в космическую бурю!", True, (255, 255, 255))
            text_rect = welcome_text.get_rect(center=(WIDTH // 2, 60))
            text_rect.top = 80
            self.screen.blit(welcome_text, text_rect)

            # Кнопка настройки
            settings_btn = pygame.image.load('../assets/images/settings.png')
            settings_btn = pygame.transform.scale(settings_btn, (60, 60))
            settings_btn_rect = settings_btn.get_rect()
            settings_btn_rect.topleft = (20, 70)
            self.screen.blit(settings_btn, (20, 70))

            # Кнопка для начала игры
            button_text = self.button_font.render("Начать игру", True, (255, 255, 255))
            button_rect = button_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 250))
            pygame.draw.rect(self.screen, (0, 128, 0), button_rect.inflate(20, 20))  # Кнопка
            self.screen.blit(button_text, button_rect)

            # Кнопка слева
            left_arrow = pygame.image.load('../assets/images/arrow.png')
            left_arrow = pygame.transform.scale(left_arrow, (200, 200))
            l_arrow_rect = left_arrow.get_rect(center=(WIDTH // 2 - 280, HEIGHT // 2))

            self.screen.blit(left_arrow, l_arrow_rect)

            # Кнопка справа
            right_arrow = pygame.image.load('../assets/images/arrow.png')
            right_arrow = pygame.transform.scale(right_arrow, (200, 200))
            right_arrow = pygame.transform.flip(right_arrow, True, False)
            r_arrow_rect = right_arrow.get_rect(center=(WIDTH // 2 + 300, HEIGHT // 2))

            self.screen.blit(right_arrow, r_arrow_rect)

            # Скин на выбор
            skin_name = img_skin_names[ skin_index % (len(img_skin_names)) ]
            skin_img = pygame.image.load(f'../assets/images/{skin_name}.png')
            skin_img = pygame.transform.scale(skin_img, (300, 300))
            skin_img_rect = skin_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))

            self.screen.blit(skin_img, skin_img_rect)

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
                        settings()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return

                
            pygame.display.flip()

    def show_game_over_screen(self):
        """ Отображение конца игры. """
        pygame.display.set_caption("Game over")
        blue = (0, 0, 0)

        res_text = self.font.render(f"Твой результат: {SCORE}", True, (255, 255, 255))
        text_rect = res_text.get_rect(center=(WIDTH // 2, 60))
        text_rect.top = 80

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
            pygame.draw.rect(self.screen, (41, 49, 51), button_rect.inflate(20, 20))  # Кнопка
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
            self.screen.blit(res_text, text_rect)
            all_sprites.draw(self.screen)
            pygame.display.flip()
            clock.tick(60)
        pygame.quit()

    def run(self):
        self.show_auth_screen()
        
        if user_name:
            self.show_welcome_screen()
            self.main_game()

    def main_game(self):
        """ Основной игровой цикл. """
        global ASTEROID_SPEED, COEFFICIENT, SCORE
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()

        background_image = pygame.image.load('../assets/images/background.png').convert()
        background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
        # Группы спрайтов
        all_sprites = pygame.sprite.Group()
        asteroids = pygame.sprite.Group()
        bullets = pygame.sprite.Group()

        # Создание игрока
        player = Player()
        all_sprites.add(player)

        # Основной игровой цикл
        SCORE = 0
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bullet = player.shoot()  # Выстрел
                        all_sprites.add(bullet)
                        bullets.add(bullet)
            elapsed_time = pygame.time.get_ticks() - start_time  # Время в миллисекундах

            # Преобразуем в секунды
            elapsed_seconds = elapsed_time / 1000.0
            if elapsed_seconds > 20 * COEFFICIENT:
                SCORE += 75
                ASTEROID_SPEED = ASTEROID_SPEED * (COEFFICIENT + 1)
                COEFFICIENT += 1


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
                    SCORE += len(hit_asteroids)

            # Проверка на столкновение игрока с астероидами
            if pygame.sprite.spritecollideany(player, asteroids):
                self.show_game_over_screen()

            # Отрисовка
            self.screen.blit(background_image, (0,0))
            all_sprites.draw(self.screen)
            player.draw(self.screen)

            # Отображение счета
            font = pygame.font.Font(None, 36)
            text = font.render(f'Score: {SCORE}', True, WHITE)
            self.screen.blit(text, (10, 10))

            pygame.display.flip()
            clock.tick(FPS)


        self.running = False
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
