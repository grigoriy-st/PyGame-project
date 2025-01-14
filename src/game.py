import pygame
import sys

class Game:
    def __init__(self):
        pygame.init()
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Космическая буря")
        self.running = True
        self.font = pygame.font.Font(None, 50)
        self.button_font = pygame.font.Font(None, 48)

    def show_welcome_screen(self):
        while True:
            self.screen.fill((0, 0, 0))

            # Главный текст
            welcome_text = self.font.render("Добро пожаловать в космическую бурю!", True, (255, 255, 255))
            text_rect = welcome_text.get_rect(center=(self.width // 2, self.height // 2 - 50))
            self.screen.blit(welcome_text, text_rect)

            # Кнопка для начала игры
            button_text = self.button_font.render("Начать игру", True, (255, 255, 255))
            button_rect = button_text.get_rect(center=(self.width // 2, self.height // 2 + 50))
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

            pygame.display.flip()

    def run(self):
        self.show_welcome_screen()
        self.main_game()

    def main_game(self):
        """ Основной игровой цикл. """
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Заполнение экрана цветом
            self.screen.fill((0, 0, 0))

            # дальнейшая логика
            pygame.display.flip()

        pygame.quit()