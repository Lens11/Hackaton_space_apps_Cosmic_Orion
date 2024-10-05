import pygame
import random
import os


WIDTH = 800
HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


class AssetManager:
    @staticmethod
    def load_image(name, game_name, width, height):
        fullname = os.path.join('assets', game_name, name)
        image = pygame.image.load(fullname).convert_alpha()
        return pygame.transform.scale(image, (width, height))



class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Mini Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 18)
        self.background = AssetManager.load_image('background.png','menu', WIDTH, HEIGHT)
        self.all_sprites = pygame.sprite.Group()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.all_sprites.draw(self.screen)
        fps_text = self.font.render(f'FPS: {int(self.clock.get_fps())}', True, pygame.Color("coral"))
        self.screen.blit(fps_text, (10, 0))
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)