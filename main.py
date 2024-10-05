import pygame
import random
import space_shooter_c1 as space_shooter
import breakout_c1 as breakout
import os
import utils
import ground_fighter_c1 as ground_fighter

pygame.init()

# Constants
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





class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.background = utils.AssetManager.load_image('background.png','menu', WIDTH, HEIGHT)
        self.font = pygame.font.SysFont("Arial", 32)
        self.games = [
    ("Shooter Game", space_shooter.ShooterGame),
    ("Breakout Game", breakout.BreakoutGame), 
    ("Ground Fighter", ground_fighter.GroundFighterGame), 
    
]
        self.buttons = self.create_buttons()

    def create_buttons(self):
        buttons = []
        for i, (game_name, _) in enumerate(self.games):
            y = HEIGHT // 2 - (len(self.games) * 60) // 2 + i * 60
            buttons.append(Button(WIDTH // 2 - 100, y, 200, 50, game_name, GREEN, WHITE, 32))
        buttons.append(Button(WIDTH // 2 - 100, HEIGHT - 100, 200, 50, "Quit", RED, WHITE, 32))
        return buttons

    def run(self):
        while True:
            self.screen.blit(self.background, (0, 0))
            for button in self.buttons:
                button.draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, button in enumerate(self.buttons[:-1]):
                        if button.is_clicked(event.pos):
                            return self.games[i][1]
                    if self.buttons[-1].is_clicked(event.pos):
                        return None


class Button:
    def __init__(self, x, y, width, height, text, color, text_color, font_size):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.SysFont("Arial", font_size)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    menu = Menu(screen)
    
    while True:
        game_class = menu.run()
        if game_class is None:
            break
        
        game = game_class(screen)
        result = game.run()
        
        if result == "quit":
            break
        
        # Show game over screen
        font = pygame.font.SysFont("Arial", 64)
        if result == "win":
            text = font.render("You Win!", True, GREEN)
        else:
            text = font.render("Game Over", True, RED)
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
        screen.blit(game.background, (0, 0))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(2000)

    pygame.quit()

if __name__ == "__main__":
    main()