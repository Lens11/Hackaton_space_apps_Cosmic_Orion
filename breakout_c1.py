import pygame
import random
import sys
import utils

# Constants
WIDTH = 800
HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)
MEDIUM_BLUE = (0, 100, 255)
DARK_BLUE = (0, 0, 139)

# Palette de couleurs
color_palette = [LIGHT_BLUE, MEDIUM_BLUE, DARK_BLUE]

class BreakoutGame(utils.Game):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen

        # Barre
        self.paddle_width = 120
        self.paddle_height = 15
        self.paddle_x = (WIDTH - self.paddle_width) // 2
        self.paddle_y = HEIGHT - 30
        self.paddle_speed = 8

        # Balle
        self.ball_radius = 10
        self.ball_x = WIDTH // 2
        self.ball_y = HEIGHT // 2
        self.ball_speed_x = 4
        self.ball_speed_y = -4

        # Blocs
        self.block_width = 70
        self.block_height = 25
        self.blocks = []
        self.create_blocks()

        # Variables de jeu
        self.score = 0
        self.lives = 5  # Nombre de vies
        self.font = pygame.font.Font(None, 36)

    def create_blocks(self):
        # Création des blocs
        for row in range(5):
            for col in range(WIDTH // (self.block_width + 10)):
                block_x = col * (self.block_width + 10) + 35
                block_y = row * (self.block_height + 10) + 50
                color = color_palette[row % len(color_palette)]
                block = pygame.Rect(block_x, block_y, self.block_width, self.block_height)
                self.blocks.append((block, color))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.paddle_x > 0:
            self.paddle_x -= self.paddle_speed
        if keys[pygame.K_RIGHT] and self.paddle_x < WIDTH - self.paddle_width:
            self.paddle_x += self.paddle_speed

        # Déplacement de la balle
        self.ball_x += self.ball_speed_x
        self.ball_y += self.ball_speed_y

        # Rebonds sur les murs
        if self.ball_x - self.ball_radius <= 0 or self.ball_x + self.ball_radius >= WIDTH:
            self.ball_speed_x = -self.ball_speed_x
        if self.ball_y - self.ball_radius <= 0:
            self.ball_speed_y = -self.ball_speed_y

        # Perte de vie si la balle sort par le bas
        if self.ball_y + self.ball_radius >= HEIGHT:
            self.lives -= 1
            if self.lives > 0:
                self.reset_ball()
            else:
                return "game_over"

        # Collision avec la barre
        paddle_rect = pygame.Rect(self.paddle_x, self.paddle_y, self.paddle_width, self.paddle_height)
        if paddle_rect.collidepoint(self.ball_x, self.ball_y + self.ball_radius):
            self.ball_speed_y = -self.ball_speed_y
            # Ajustement de l'angle de rebond
            self.ball_speed_x += (self.ball_x - (self.paddle_x + self.paddle_width / 2)) / 10
            self.ball_speed_x = max(min(self.ball_speed_x, 5), -5)

        # Gestion des collisions avec les blocs
        for block, color in self.blocks[:]:
            if block.collidepoint(self.ball_x, self.ball_y):
                self.ball_speed_y = -self.ball_speed_y
                self.blocks.remove((block, color))
                self.score += 10

        # Vérifier si tous les blocs sont détruits (victoire)
        if not self.blocks:
            return "win"

    def reset_ball(self):
        self.ball_x, self.ball_y = WIDTH // 2, HEIGHT // 2
        self.ball_speed_y = -abs(self.ball_speed_y)

    def draw(self):
        self.screen.fill(BLACK)

        # Dessin des blocs
        for block, color in self.blocks:
            pygame.draw.rect(self.screen, color, block)

        # Dessin de la barre
        pygame.draw.rect(self.screen, BLUE, pygame.Rect(self.paddle_x, self.paddle_y, self.paddle_width, self.paddle_height))

        # Dessin de la balle
        pygame.draw.circle(self.screen, WHITE, (int(self.ball_x), int(self.ball_y)), self.ball_radius)

        # Affichage du score et des vies
        self.draw_text(f"Score: {self.score}", 10, 10)
        self.draw_text(f"Vies: {self.lives}", WIDTH - 100, 10)

        pygame.display.flip()

    def draw_text(self, text, x, y):
        surface = self.font.render(text, True, WHITE)
        self.screen.blit(surface, (x, y))

    def run(self):
        result = None
        while result is None:
            result = self.handle_events()
            if result is False:
                return "quit"
            result = self.update()
            self.draw()
            self.clock.tick(FPS)
        return result
