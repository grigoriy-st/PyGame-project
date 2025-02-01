import sys
import pygame
from game import Game
from settings import (
    BLACK, WHITE,
    WIDTH, HEIGHT,
)
class Auth_Screen(Game):
    def __init__(self):
        super().__init__()

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
                            return
                        
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode

            welcome_text = self.font.render("Добро пожаловать в космическую бурю!",
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
            # self.screen.blit(button_text, button_rect)
            text_surface = base_font.render(user_text, True, (255, 255, 255))
            self.screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))
            input_rect.w = max(100, text_surface.get_width()+10)
            pygame.display.flip()
            # 60 frames should be passed.
            clock.tick(60)