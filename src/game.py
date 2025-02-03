import os
import pygame
import sys
import random
# from moviepy import VideoFileClip

from db_manager import DBManager
from player import Player, img_skin_names
from asteroid import ASTEROID_SPAWN_RATE
from bullet import BULLET_SPEED
from asteroid import Asteroid
from sprite import Sprite
from explosion import Explosion
from coin import Coin, COIN_SPAWN_RATE


from settings import (
    WIDTH, HEIGHT,
    BLACK, WHITE,
    user_name
)
# Переменные игры

FPS = 60



class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Космическая буря")
        self.running = True
        self.font = pygame.font.Font(None, 50)
        self.button_font = pygame.font.Font(None, 48)

        self.db_mng = DBManager()  # Менеджер работы с БД
        self.user_name = user_name

        self.skin_ID = 0
        self.score = 0
        self.coins_counter = 0

    def show_auth_screen(self):
        """ Отображение окна авторизации. """
        global user_name

        self.screen.fill(BLACK)
        clock = pygame.time.Clock()
        # Шрифт
        base_font = pygame.font.Font(None, 32)
        error_font = pygame.font.Font(None, 28)
        # Текстовые переменные
        user_text = ''
        error_message = ''  # Сообщение об ошибке
        # Цвета
        color_active = pygame.Color('lightskyblue3')
        color_passive = pygame.Color('chartreuse4')
        color = color_passive
        # Переменные состояний
        active = False

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
                        if user_name == '':
                            error_message = 'Ошибка: имя не может быть пустым!'
                        else:
                            error_message = ''
                            self.user_name = user_name
                            return

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode


            welcome_text = self.font.render(
                "Добро пожаловать в космическую бурю!",
                True, (255, 255, 255))
            text_rect = welcome_text.get_rect(
                                    center=(WIDTH // 2, HEIGHT // 2 - 200)
                                    )
            text2 = self.font.render("Введите своё имя:", True, (255, 255, 255))
            text2_rect = welcome_text.get_rect(
                                    center=(WIDTH // 2 + 200, HEIGHT // 2 - 30)
                                    )
            input_width = 200
            input_height = 32
            input_rect = pygame.Rect((WIDTH // 2 - 90), (HEIGHT // 2),
                                     input_width, input_height)
            button_text = self.button_font.render("Войти", True, (0, 0, 0))
            button_rect = button_text.get_rect(center=(
                                                WIDTH // 2, HEIGHT // 2 + 200)
                                               )

            self.screen.fill(BLACK)
            pygame.draw.rect(self.screen, (0, 255, 0),
                             button_rect.inflate(20, 20))  # Кнопка
            self.screen.blit(button_text, button_rect)
            self.screen.blit(welcome_text, text_rect)
            self.screen.blit(text2, text2_rect)

            if error_message:  # Отображение ошибки ввода
                error_surface = error_font.render(
                                error_message, True, (255, 0, 0))
                error_rect = error_surface.get_rect(
                            center=(WIDTH // 2, HEIGHT // 2 + 250))
                self.screen.blit(error_surface, error_rect)

            if active:
                color = color_active
            else:
                color = color_passive

            pygame.draw.rect(self.screen, color, input_rect)
            text_surface = base_font.render(user_text, True, (255, 255, 255))
            self.screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))
            input_rect.w = max(100, text_surface.get_width()+10)
            pygame.display.flip()

            clock.tick(60)

    def show_welcome_screen(self):
        """ Отображение приветственного окна. """
        global skin_index, img_skin_names
        while True:
            self.screen.fill((0, 0, 0))

            # Главный текст
            welcome_text = self.font.render(
                f"{user_name}, добро пожаловать в космическую бурю!",
                True, (255, 255, 255))
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
            button_text = self.button_font.render("Начать игру",
                                                  True, (255, 255, 255))
            button_rect = button_text.get_rect(
                                center=(WIDTH // 2, HEIGHT // 2 + 250))
            pygame.draw.rect(self.screen, (0, 128, 0),
                             button_rect.inflate(20, 20))  # Кнопка
            self.screen.blit(button_text, button_rect)

            # Кнопка слева
            left_arrow = pygame.image.load('../assets/images/arrow.png')
            left_arrow = pygame.transform.scale(left_arrow, (200, 200))
            l_arrow_rect = left_arrow.get_rect(
                center=(WIDTH // 2 - 280, HEIGHT // 2))

            self.screen.blit(left_arrow, l_arrow_rect)

            # Кнопка справа
            right_arrow = pygame.image.load('../assets/images/arrow.png')
            right_arrow = pygame.transform.scale(right_arrow, (200, 200))
            right_arrow = pygame.transform.flip(right_arrow, True, False)
            r_arrow_rect = right_arrow.get_rect(
                center=(WIDTH // 2 + 300, HEIGHT // 2))

            self.screen.blit(right_arrow, r_arrow_rect)

            # Скин на выбор
            skin_name = img_skin_names[self.skin_ID % (len(img_skin_names))]
            skin_img = pygame.image.load(f'../assets/images/{skin_name}.png')
            skin_img = pygame.transform.scale(skin_img, (300, 300))
            skin_img_rect = skin_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))

            self.screen.blit(skin_img, skin_img_rect)

            # Отображение рекорда текущего игрока
            last_record, is_exists_record = self.db_mng.get_last_score(user_name)
            if is_exists_record:
                l_score_lbl_text = self.button_font.render(
                    f"Твой рекорд: {last_record}", True, (255, 255, 255))
                lbl_score_rect = l_score_lbl_text.get_rect(
                                    center=(WIDTH // 2, 160))
                self.screen.blit(l_score_lbl_text, lbl_score_rect)

            # Отображение рекорда лучшего игрока
            # record_holder_name, record = self.db_mng.get_best_score()
            best_score_record = self.db_mng.get_best_score()
            if best_score_record:
                record_holder_name, record_score = best_score_record
                record_among_all_text = self.button_font.render(
                    'Лучший игрок: {}, набрал {} очков'.format(
                        record_holder_name, record_score),
                    True, (255, 255, 255))
                record_among_all_rect = record_among_all_text.get_rect(
                                        center=(WIDTH // 2, 200))
                self.screen.blit(record_among_all_text, record_among_all_rect)

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
                        self.skin_ID -= 1

                    if r_arrow_rect.collidepoint(event.pos):
                        self.skin_ID += 1

                    if settings_btn_rect.collidepoint(event.pos):
                        # Работа кнопки настроек
                        # print("Нажата кнопка настроек")
                        ...

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return

            pygame.display.flip()

    def show_game_over_screen(self):
        """ Отображение конца игры. """

        pygame.display.set_caption("Game over")
        blue = (0, 0, 0)

        res_text = self.font.render(f"Твой результат: {self.score}",
                                    True, (255, 255, 255))
        text_rect = res_text.get_rect(center=(WIDTH // 2, 60))
        text_rect.top = 80
        coins_label = self.font.render(
            f"Собрано монет: {self.coins_counter}",
            True, (255, 255, 255))
        c_label_rect = res_text.get_rect(center=(WIDTH // 2, 60))
        c_label_rect.top = 150

        # Работа с БД
        last_score, is_exists_record = self.db_mng.get_last_score(self.user_name)
        if is_exists_record and last_score < self.score:  # Лучшая ли игра у пользователя?
            self.db_mng.update_score(
                self.user_name, self.score, self.coins_counter)
        elif not is_exists_record:
            self.db_mng.add_record(
                self.user_name, self.score, self.coins_counter)

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

            button_text = self.button_font.render("Начать новую игру",
                                                  True, (255, 255, 255))
            button_rect = button_text.get_rect(
                                    center=(WIDTH // 2, HEIGHT // 2 + 200))
            pygame.draw.rect(self.screen, (41, 49, 51),
                             button_rect.inflate(20, 20))  # Кнопка
            self.screen.blit(button_text, button_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.db_mng.update_score(self.user_name, self.score, self.coins_counter)
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        self.show_welcome_screen()
                        self.main_game()  # начало новой игры
                        break

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.show_welcome_screen()
                            self.main_game()  # начало новой игры
                            break

            all_sprites.update(clock)
            
            try:
                self.screen.blit(res_text, text_rect)
                self.screen.blit(coins_label, c_label_rect)
                all_sprites.draw(self.screen)
                pygame.display.flip()
                clock.tick(60)
            except pygame.error as e:
                print(f"Error: {e}")

        pygame.quit()

    def run(self):
        self.show_auth_screen()

        if user_name:
            self.show_welcome_screen()
            self.main_game()

    def main_game(self):
        """ Основной игровой цикл. """
        global skin_index

        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()

        background_image = pygame.image.load(
                        '../assets/images/background.png').convert()
        background_image = pygame.transform.scale(background_image,
                                                  (WIDTH, HEIGHT))
        # Группы спрайтов
        all_sprites = pygame.sprite.Group()
        asteroids = pygame.sprite.Group()
        coins = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        explosions = pygame.sprite.Group()

        # Создание игрока
        player = Player(self.skin_ID)
        all_sprites.add(player)

        # Переменные игры
        asteroid_speed = 2
        coefficient = 1
        self.score = 0
        self.coins_counter =0

        # Основной игровой цикл
        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif (event.type == pygame.MOUSEBUTTONDOWN or
                      event.type == pygame.KEYDOWN):
                    if event.key == pygame.K_SPACE:
                        bullet = player.shoot()  # Выстрел
                        all_sprites.add(bullet)
                        bullets.add(bullet)
            # Время в миллисекундах
            elapsed_time = pygame.time.get_ticks() - start_time
            elapsed_seconds = elapsed_time / 1000.0  # Преобразуем в секунды

            if elapsed_seconds > 15 * coefficient:
                # Увеличиваем скорость плавно
                new_speed = asteroid_speed + (coefficient / 2)
                asteroid_speed = min(new_speed, 20)
                coefficient += 1
                self.score += 25

            # Отображение астероидов
            if random.randint(1, ASTEROID_SPAWN_RATE) == 1:
                asteroid = Asteroid(asteroid_speed, coefficient)
                all_sprites.add(asteroid)
                asteroids.add(asteroid)

            # Отображение монет
            if random.randint(1, COIN_SPAWN_RATE) == 1:
                coin = Coin(asteroid_speed, coefficient)
                all_sprites.add(coin)
                coins.add(coin)

            # Проверка на столкновения
            for bullet in bullets:
                hit_asteroids = pygame.sprite.spritecollide(
                    bullet, asteroids, True)
                if hit_asteroids:
                    bullets.remove(bullet)
                    bullet.kill_asteroid_sound()
                    bullet.kill()
                    self.score += 1

                    for asteroid in hit_asteroids:
                        asteroid_width = asteroid.rect.width
                        asteroid_height = asteroid.rect.height

                        # Взрыв в позиции астероида
                        explosion = Explosion(asteroid.rect.centerx,
                                              asteroid.rect.centery,
                                              '../assets/gifs/explosion.gif',
                                              width=asteroid_width,
                                              height=asteroid_height)
                        explosions.add(explosion)

            for coin in coins:
                is_collected_coin = pygame.sprite.spritecollide(
                    player, coins, True)
                if is_collected_coin:
                    coin.sound_of_collecting_coin()
                    coin.kill()
                    self.coins_counter += 1

            # Обновление спрайтов
            all_sprites.update()
            explosions.update()

            # Проверка на столкновение игрока с астероидами
            if pygame.sprite.spritecollideany(player, asteroids):
                self.show_game_over_screen()

            # Отрисовка
            self.screen.blit(background_image, (0, 0))
            all_sprites.draw(self.screen)
            player.draw(self.screen)
            explosions.draw(self.screen)

            # Отображение счета
            font = pygame.font.Font(None, 40)
            score_label = font.render(f'Score: {self.score}', True, WHITE)
            self.screen.blit(score_label, (10, 10))
            coin_counter_label = font.render(
                f'Coins: {self.coins_counter}', True, WHITE)
            self.screen.blit(coin_counter_label, (10, 35))

            pygame.display.flip()
            clock.tick(FPS)

        self.running = False
        self.db_mng.close()
        pygame.quit()



if __name__ == "__main__":
    game = Game()
    game.run()
