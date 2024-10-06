import pygame
import space_shooter_c1 as space_shooter
import utils
import ground_fighter_c1 as ground_fighter
import image_display_c1 as im_disp
import image_display_action_c1 as im_action
import space_jumper_c1 as space_jumper

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
        self.background = utils.AssetManager.load_image('background.jpg', 'menu', WIDTH, HEIGHT)
        self.font = pygame.font.SysFont("britannic", 32)

        # Dictionary to track unlocked levels
        self.unlocked_levels = {
            'space_shooter_1': [False, False, False],
            'space_shooter_1_info' : [False, False, False],
            'ground_fighter_1': [False, False, False],
            'ground_fighter_1_info' : [False, False, False],
            'space_shooter_2': [False, False, False],
            'space_shooter_2_info': [False, False, False],
            'ground_fighter_2': [False, False, False],
            'ground_fighter_2_info': [False, False, False],
            'simple_backgroundAction': [True, True, True, True]
        }        
        
        self.font = pygame.font.SysFont("britannic", 24)
        
        self.starting_images = {
            0 : ('Gas_Giant.png', "Gas Giant Exoplanet"),
            1 : ('Neptunian.png', "Neptunian Exoplanet"),
            2 : ('Terrestrial.png', "Terrestrial Exoplanet"),
            3 : ('Super_Earth.png', "Super-Earth Exoplanet")
        }
        
        self.selector_image = {
            0: 'Gas_GiantBar.png',
            1: 'NeptunianBar.png',
            2: 'TerrestrialBar.png',
            3: 'Super_EarthBar.png'
        }

        self.games = [
            [
                ("space_shooter_1", lambda s: space_jumper.SpaceJumperGame(s, difficulty=1), "51PegasiB.png", "51 Pegasi B", "51_Pegasi_BSpec.png"),
                ("space_shooter_1", lambda s: space_shooter.ShooterGame(s, difficulty=2), "KELT9B.png", "KELT-9B", "KELT-9BSpec.png"),
                ("space_shooter_1", lambda s: space_shooter.ShooterGame(s, difficulty=3), "HIP.png", "HIP 11915B", "HIP_11915BSpec.png"),
            ],
            [
                ("ground_fighter_1", lambda s: ground_fighter.GroundFighterGame(s, difficulty=1), "K2263b.png", "K2-263b", "K2-263bSpec.png"),
                ("ground_fighter_1", lambda s: ground_fighter.GroundFighterGame(s, difficulty=2), "Gliese436b.png", "Gliese 436b", "GlieseSpec.png"),
                ("ground_fighter_1", lambda s: ground_fighter.GroundFighterGame(s, difficulty=3), "HATP11b.png", "HAT-P-11b", "HATSpec.png"),
            ],
            [
                ("space_shooter_2", lambda s: space_shooter.ShooterGame(s, difficulty=1), "TRAPPIST1.png", "TRAPPIST-1", "TRAPPISTSpec.png"),
                ("space_shooter_2", lambda s: space_shooter.ShooterGame(s, difficulty=2), "Kepler186f.png", "Kepler-186f", "Kepler-186fSpec.png"),
                ("space_shooter_2", lambda s: space_shooter.ShooterGame(s, difficulty=3), "ProximaCentaurib.png", "Proxima Centauri b", "ProximaSpec.png"),
            ],
            [
                ("ground_fighter_2", lambda s: ground_fighter.GroundFighterGame(s, difficulty=1), "k2.png", "K2-131b", "k2Spec.png"),
                ("ground_fighter_2", lambda s: ground_fighter.GroundFighterGame(s, difficulty=2), "kepler.png", "Kepler-452b", "keplerSpec.png"),
                ("ground_fighter_2", lambda s: ground_fighter.GroundFighterGame(s, difficulty=3), "LHS.png", "LHS 1140b", "LHSSpec.png"),
            ]
        ]
        self.buttons = self.create_buttons()
        self.hovered_button = None
            
    def create_buttons(self):
        buttons = []
        row_height = (HEIGHT - 100) // (len(self.games) + 1)
        button_spacing = 150
        button_width = 70
        for row, game_column in enumerate(self.games):
            y = row_height * (row + 1) - button_width // 2 + 100
            
            # Create the SimpleBackgroundGame button for this row
            image_name, display_name = self.starting_images[row]
            selector_image = self.selector_image[row]
            buttons.append(ImageButton(100, y, selector_image, scale=0.5, 
                                       game_class=lambda s, img=image_name: im_action.SimpleBackgroundActionGame(s, image=img, menu=self), 
                                       display_name=display_name, unlocked=True, 
                                       game_key="simple_backgroundAction", size=(175, 80)))
            
            # Add progress bar for SimpleBackgroundGame
            BAR_SIZE = 125
            PADDING = 125
            progress = (sum(self.unlocked_levels["simple_backgroundAction"]) - 1) / len(self.unlocked_levels["simple_backgroundAction"])
            bar_width = int(BAR_SIZE * progress)
            t = progress
            COLOR = (int(255*(1 - t)), int(255*t), 0)
            pygame.draw.rect(self.screen, COLOR, (PADDING, y, bar_width, 20))
            pygame.draw.rect(self.screen, WHITE, (PADDING, y, BAR_SIZE, 20), 2)
            
            for col, (game_key, game_class, image_name, display_name, spec_name) in enumerate(game_column):
                x = 300 + col * button_spacing
                unlocked = self.unlocked_levels[game_key][col]
                unlocked_info = self.unlocked_levels[game_key+"_info"][col]
                buttons.append(ImageButton(x, y, image_name, scale=0.5, game_class=game_class, display_name=display_name, unlocked=unlocked, game_key=game_key))
                buttons.append(ImageButton(x + 75,  y+10, "choice.png", scale=0.5, game_class=None, display_name="MCQ", unlocked=False, size=(40,40)))
                buttons.append(ImageButton(x + 50,  y-30, "information.png", scale=0.5, 
                                           game_class=lambda s, img=spec_name: im_disp.SimpleBackgroundGame(s, image=img, menu=self), 
                                           display_name=display_name, unlocked=unlocked_info, 
                                           game_key=game_key+"_info", size=(20,20)))
                
        # Add Quit button
        buttons.append(ImageButton(WIDTH - 80,  50, "quit_button.png", scale=0.5, game_class=None, display_name="Exit Game", unlocked=True, size=(30,30)))
        return buttons
    
    def run(self):
        font = pygame.font.SysFont("britannic", 64)

        while True:
            self.screen.blit(self.background, (0, 0))

            mouse_pos = pygame.mouse.get_pos()
            self.hovered_button = None

            for button in self.buttons:
                button.set_hover(button.rect.collidepoint(mouse_pos))
                if button.rect.collidepoint(mouse_pos):
                    self.hovered_button = button
                button.draw(self.screen)

            # Draw progress bars
            self.draw_progress_bars()

            text_surface = font.render('ExoExplorer', True, WHITE)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 4 - 85))
            self.screen.blit(text_surface, text_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.is_clicked(event.pos) and button.unlocked:
                            if button.game_class is None:  # Quit button
                                return None
                            return button.game_class
                        
    def draw_progress_bars(self):
        BAR_SIZE = 90
        PADDING = 65
        row_height = (HEIGHT - 100) // (len(self.games) + 1)
        for row, game_column in enumerate(self.games):
            y = row_height * (row + 1) - 35 + 100  # Adjusted y position
            game_key = game_column[0][0]
            progress = (sum(self.unlocked_levels[game_key]) - 1) / len(self.unlocked_levels[game_key])
            if progress < 0: progress = 0
            bar_width = int(BAR_SIZE * progress)
            t = progress
            COLOR = (int(255*(1 - t)), int(255*t), 0)
            pygame.draw.rect(self.screen, COLOR, (PADDING, y+25, bar_width, 20))
            pygame.draw.rect(self.screen, WHITE, (PADDING, y+25, BAR_SIZE, 20), 2)
            
            percentage = int(progress * 100)
            percentage_text = self.font.render(f"{percentage}%", True, WHITE)
            text_rect = percentage_text.get_rect(midleft=(PADDING + BAR_SIZE + 10, y + 35))
            self.screen.blit(percentage_text, text_rect)

class ImageButton:
    def __init__(self, x, y, image_name, scale=1, game_class=None, display_name=None, unlocked=True, game_key=None, size=(70, 70)):
        self.size = size
        self.original_image = utils.AssetManager.load_image(image_name, 'menu', self.size[0], self.size[1])  # Load without scaling
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
            hover_image = pygame.transform.scale(self.original_image, (self.size[0] + 10, self.size[1] + 10))  # Create a slightly larger version of the image for hover effect
            self.image = hover_image
            self.rect = self.image.get_rect(center=self.rect.center)  # Adjust position to keep the button centered
        else:
            self.image = pygame.transform.scale(self.original_image, (self.size[0], self.size[1]))  # Reset to original size
            self.rect = self.image.get_rect(center=self.rect.center)

class Homepage:
    def __init__(self, screen):
        self.screen = screen
        self.background = utils.AssetManager.load_image('Homepage.png', 'menu', WIDTH, HEIGHT)
        self.start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 175, 200, 60)
        self.start_button_image = utils.AssetManager.load_image('START.png', 'menu', 200, 60)
        self.displayed = False

    def run(self):
        clock = pygame.time.Clock()
        while not self.displayed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button.collidepoint(event.pos):
                        self.displayed = True  # Start button clicked, proceed to menu

            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.start_button_image, self.start_button)
            pygame.display.flip()
            clock.tick(FPS)
        return "menu"  # Proceed to the menu after the homepage is shown once


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    
    pygame.display.set_caption("ExoExplorer")
    pygame.display.set_icon(pygame.image.load('./assets/menu/icon.png'))
    homepage = Homepage(screen)
    menu = Menu(screen)
    homepage_displayed = False
    
    while True:
        if not homepage_displayed:
            # Show the homepage once
            if homepage.run() == "quit":
                break
            homepage_displayed = True
        game_class = menu.run()
        if game_class is None:
            break
        
        if game_class == im_action.SimpleBackgroundActionGame or game_class == im_disp.SimpleBackgroundGame:
            game = game_class(screen, menu.hovered_button.original_image.get_name(), menu)
            result = game.run()
            if isinstance(result, utils.Game):
                game = result
                result = game.run()
            elif result == "menu":
                continue
            elif result == "quit":
                break
        else:
            game = game_class(screen)
            result = game.run()
        
        if result == "quit":
            break
        elif result == "menu":
            continue
        
        # Show game over screen
        font = pygame.font.SysFont("britannic", 64)
        if result == "win":
            # Unlock the next level if available
            game_key = menu.hovered_button.game_key  # Get the game_key from the button
            unlocked_levels = menu.unlocked_levels[game_key]
            unlocked_levels_info = menu.unlocked_levels[game_key+"_info"]
            for i, unlocked in enumerate(unlocked_levels):
                if not unlocked:
                    unlocked_levels[i] = True
                    unlocked_levels_info[i] = True
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
