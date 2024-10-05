import pygame
import random
import space_shooter_c1 as space_shooter
import breakout_c1 as breakout
import os
import utils

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
        self.background = utils.AssetManager.load_image('background.png', WIDTH, HEIGHT)
        self.games = [
            [
                ("Space Shooter Easy", lambda s: space_shooter.ShooterGame(s, difficulty=1), "SS1.png", "Space Shooter Easy"),
                ("Space Shooter Medium", lambda s: space_shooter.ShooterGame(s, difficulty=2), "SS2.png", "Space Shooter Medium"),
                ("Space Shooter Hard", lambda s: space_shooter.ShooterGame(s, difficulty=3), "SS3.png", "Space Shooter Hard"),
            ],
            [
                ("Breakout Easy", lambda s: breakout.BreakoutGame(s), "SS1.png", "Breakout Easy"),
                ("Breakout Medium", lambda s: breakout.BreakoutGame(s), "SS2.png", "Breakout Medium"),
                ("Breakout Hard", lambda s: breakout.BreakoutGame(s), "SS3.png", "Breakout Hard"),
            ]
        ]
        self.buttons = self.create_buttons()
        self.hovered_button = None

    def create_buttons(self):
        buttons = []
        column_width = WIDTH // 4
        for col, game_column in enumerate(self.games):
            for row, (game_name, game_class, image_name, display_name) in enumerate(game_column):
                x = column_width * col + (column_width - 100) // 2
                y = HEIGHT // 2 - (len(game_column) * 80) // 2 + row * 120
                # On passe le nom à afficher (display_name) lors du hover
                buttons.append(ImageButton(x, y, image_name, scale=0.5, game_class=game_class, display_name=display_name))
        
        # Add Quit button
        buttons.append(ImageButton(WIDTH // 2 - 50, HEIGHT - 70, "quit_button.png", scale=0.5, game_class=None, display_name="Exit Game"))
        return buttons

    def run(self):
        font = pygame.font.SysFont("Arial", 32)
        
        while True:
            self.screen.blit(self.background, (0, 0))
            
            mouse_pos = pygame.mouse.get_pos()
            self.hovered_button = None
            for button in self.buttons:
                button.set_hover(button.rect.collidepoint(mouse_pos))
                if button.rect.collidepoint(mouse_pos):
                    self.hovered_button = button
                button.draw(self.screen)
            
            # Si un bouton est survolé, afficher le nom du mini-jeu
            if self.hovered_button and self.hovered_button.display_name is not None:
                game_name_text = f"{self.hovered_button.display_name}"
                text_surface = font.render(game_name_text, True, WHITE)
                text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 4 - 75))
                self.screen.blit(text_surface, text_rect)
            
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.is_clicked(event.pos):
                            if button.game_class is None:  # Quit button
                                return None
                            return button.game_class

class ImageButton:
    def __init__(self, x, y, image_name, scale=1, game_class=None, display_name=None):
        self.original_image = utils.AssetManager.load_image(image_name, 70, 70)  # Load without scaling
        width = int(self.original_image.get_width() * scale)
        height = int(self.original_image.get_height() * scale)
        self.image = pygame.transform.scale(self.original_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.game_class = game_class
        self.display_name = display_name  # Store the name to display

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def set_hover(self, is_hovering):
        if is_hovering:
            # Create a slightly larger version of the image for hover effect
            hover_image = pygame.transform.scale(self.original_image, 
                                                 (110, 110))
            self.image = hover_image
            # Adjust position to keep the button centered
            self.rect = self.image.get_rect(center=self.rect.center)
        else:
            # Reset to original size
            self.image = pygame.transform.scale(self.original_image, (100, 100))
            self.rect = self.image.get_rect(center=self.rect.center)

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game Launcher")
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
