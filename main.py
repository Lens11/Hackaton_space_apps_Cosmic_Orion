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
GRAY = (100, 100, 100)

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.background = utils.AssetManager.load_image('background.png', 'menu', WIDTH, HEIGHT)
        self.font = pygame.font.SysFont("Arial", 32)

        # Dictionary to track unlocked levels
        self.unlocked_levels = {
            'space_shooter': [True, False, False],  # Only the first level is unlocked initially
            'breakout': [True, False, False],
            'ground_fighter': [True, False, False]
        }

        self.games = [
            [
                ("space_shooter", lambda s: space_shooter.ShooterGame(s, difficulty=1), "SS1.png", "Space Shooter Easy"),
                ("space_shooter", lambda s: space_shooter.ShooterGame(s, difficulty=2), "SS2.png", "Space Shooter Medium"),
                ("space_shooter", lambda s: space_shooter.ShooterGame(s, difficulty=3), "SS3.png", "Space Shooter Hard"),
            ],
            [
                ("breakout", lambda s: breakout.BreakoutGame(s), "SS1.png", "Breakout Easy"),
                ("breakout", lambda s: breakout.BreakoutGame(s), "SS2.png", "Breakout Medium"),
                ("breakout", lambda s: breakout.BreakoutGame(s), "SS3.png", "Breakout Hard"),
            ],
            [
                ("ground_fighter", lambda s: ground_fighter.GroundFighterGame(s), "SS1.png", "Ground Fighter Easy"),
                ("ground_fighter", lambda s: ground_fighter.GroundFighterGame(s), "SS2.png", "Ground Fighter Medium"),
                ("ground_fighter", lambda s: ground_fighter.GroundFighterGame(s), "SS3.png", "Ground Fighter Hard"),
            ]
        ]
        self.buttons = self.create_buttons()
        self.hovered_button = None

    def create_buttons(self):
        buttons = []
        row_height = (HEIGHT - 100) // (len(self.games) + 1)  # Divide the screen height into rows for each game category
        button_spacing = 150  # Space between buttons horizontally
        button_width = 70  # Width of each button

        for row, game_column in enumerate(self.games):
            y = row_height * (row + 1) - button_width // 2 + 100  # Position buttons vertically based on the row

            for col, (game_key, game_class, image_name, display_name) in enumerate(game_column):
                x = 220 + col * button_spacing  # Horizontal placement

                # Check if this level is unlocked
                unlocked = self.unlocked_levels[game_key][col]

                # Create the button, pass the unlocked status and the game_key
                buttons.append(ImageButton(x, y, image_name, scale=0.5, game_class=game_class, display_name=display_name, unlocked=unlocked, game_key=game_key))

        # Add Quit button
        buttons.append(ImageButton(WIDTH - 80,  50, "quit_button.png", scale=0.5, game_class=None, display_name="Exit Game", unlocked=True))
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

            # If a button is hovered, display the name of the mini-game
            if self.hovered_button and self.hovered_button.display_name is not None:
                if self.hovered_button.unlocked:
                    game_name_text = f"{self.hovered_button.display_name}"
                else:
                    game_name_text = "Locked"
                text_surface = font.render(game_name_text, True, WHITE)
                text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 4 - 75))
                self.screen.blit(text_surface, text_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.is_clicked(event.pos) and button.unlocked:  # Check if button is unlocked
                            if button.game_class is None:  # Quit button
                                return None
                            return button.game_class

class ImageButton:
    def __init__(self, x, y, image_name, scale=1, game_class=None, display_name=None, unlocked=True, game_key=None):
        self.original_image = utils.AssetManager.load_image(image_name, 'menu', 70, 70)  # Load without scaling
        self.unlocked = unlocked
        self.game_key = game_key  # Store the game key
        if not unlocked:
            self.original_image.fill(GRAY, special_flags=pygame.BLEND_RGB_MULT)  # Gray out the image if locked
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
        if is_hovering and self.unlocked:
            hover_image = pygame.transform.scale(self.original_image, (100, 100))  # Create a slightly larger version of the image for hover effect
            self.image = hover_image
            self.rect = self.image.get_rect(center=self.rect.center)  # Adjust position to keep the button centered
        else:
            self.image = pygame.transform.scale(self.original_image, (70, 70))  # Reset to original size
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
            # Unlock the next level if available
            game_key = menu.hovered_button.game_key  # Get the game_key from the button
            unlocked_levels = menu.unlocked_levels[game_key]
            for i, unlocked in enumerate(unlocked_levels):
                if not unlocked:
                    unlocked_levels[i] = True
                    break
            menu.buttons = menu.create_buttons()  # Update buttons after unlocking
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
