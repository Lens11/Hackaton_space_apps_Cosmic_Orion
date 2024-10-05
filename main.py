import pygame
import space_shooter_c1 as space_shooter
import utils
import ground_fighter_c1 as ground_fighter
import image_display_c1 as im_disp
import image_display_action_c1 as im_action
import QCM_c1 as qcm

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
            'space_shooter_1_qcm' : [False, False, False],
            'space_shooter_1_done' : [False, False, False],
            'ground_fighter_1': [False, False, False],
            'ground_fighter_1_info' : [False, False, False],
            'ground_fighter_1_qcm' : [False, False, False],
            'ground_fighter_1_done' : [False, False, False],
            'space_shooter_2': [False, False, False],
            'space_shooter_2_info': [False, False, False],            
            'space_shooter_2_qcm' : [False, False, False],
            'space_shooter_2_done' : [False, False, False],
            'ground_fighter_2': [False, False, False],
            'ground_fighter_2_info': [False, False, False],
            'ground_fighter_2_qcm' : [False, False, False],
            'ground_fighter_2_done' : [False, False, False],
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
                ("space_shooter_1", lambda s: space_shooter.ShooterGame(s, difficulty=1), "51PegasiB.png", "51 Pegasi B", "51_Pegasi_BSpec.png",
                 lambda s: qcm.QCMGame(s, questions=[("What are gas giants primarily composed of?", ["Rock and ice", "Hydrogen and helium", "Metal and dust", "Water and carbon dioxide"]),], correct_answers=["2"])),
                ("space_shooter_1", lambda s: space_shooter.ShooterGame(s, difficulty=2), "KELT9B.png", "KELT-9B", "KELT-9BSpec.png",
                 lambda s: qcm.QCMGame(s, questions=[
        ("Which two planets in our solar system are gas giants?", ["Earth and Mars", "Jupiter and Neptune", "Jupiter and Saturn", "Venus and Uranus"]),
        ("What is a hot Jupiter?", ["A gas giant that is far from its star", "A small, rocky planet close to its star", "A gas giant orbiting close to its star, making it extremely hot", "A gas giant with a solid surface"]),
    ], correct_answers= ["3", "3"])),
                ("space_shooter_1", lambda s: space_shooter.ShooterGame(s, difficulty=3), "HIP.png", "HIP 11915B", "HIP_11915BSpec.png",
                 lambda s: qcm.QCMGame(s, questions=[
        ("How many exoplanets have scientists discovered in the last 25 years?", ["Over 500", "Over 5,600", "Over 56,000", "Over 100"]),
        ("What is the name of the youngest hot Jupiter ever found?", ["HD 209458 b", "HIP 67522 b", "Kepler-22b", "WASP-12b"]),
        ("How long does it take HIP 67522 b to orbit its star?", ["365 days", "7 days", "30 days", "90 days"]),
    ],correct_answers=["2", "2", "2"])),
            ],
            [
                ("ground_fighter_1", lambda s: ground_fighter.GroundFighterGame(s), "SS1.png", "K2-263b", "K2-263bSpec.png",
                 lambda s: qcm.QCMGame(s, questions=[
        ("What type of atmosphere do Neptunian planets typically have?", ["Oxygen-rich atmosphere", "Hydrogen and helium-dominated atmosphere", "Carbon dioxide-rich atmosphere", "Sulfur-rich atmosphere"]),
    ], correct_answers=["2"])),
                ("ground_fighter_1", lambda s: ground_fighter.GroundFighterGame(s), "SS2.png", "Gliese 436b", "GlieseSpec.png",
                 lambda s: qcm.QCMGame(s, questions=[
        ("What are mini-Neptunes?", ["Planets larger than Neptune", "Planets smaller than Neptune and bigger than Earth", "Gas giants with rocky surfaces", "Rocky planets with liquid water"]),
        ("Which two planets in our solar system are considered ice giants?", ["Earth and Mars", "Saturn and Jupiter", "Uranus and Neptune", "Mercury and Venus"]),
    ], correct_answers=["2", "3"])),
                ("ground_fighter_1", lambda s: ground_fighter.GroundFighterGame(s), "SS3.png", "HAT-P-11b", "HATSpec.png",
                 lambda s: qcm.QCMGame(s, questions=[
        ("How much larger is Neptune compared to Earth?", ["Two times the size", "Four times the size", "Six times the size", "Eight times the size"]),
        ("What chemicals are commonly found in the atmospheres of Uranus and Neptune?", ["Hydrogen and oxygen", "Water, ammonia, and methane", "Carbon dioxide and nitrogen", "Helium and sulfur"]),
        ("How far away was the ice giant exoplanet discovered in 2014?", ["1,000 light-years", "10,000 light-years", "25,000 light-years", "100,000 light-years"]),
    ], corect_answers=["2", "2", "3"])),
            ],
            [
                ("space_shooter_2", lambda s: space_shooter.ShooterGame(s, difficulty=1), "SS1.png", "TRAPPIST-1", "TRAPPISTSpec.png",
                 lambda s: qcm.QCMGame(s, questions=[
        ("What are terrestrial planets primarily composed of?", ["Gas and ice", "Rock, silicate, water, and/or carbon", "Hydrogen and helium", "Metal and dust"]),
    ], correct_answers=["2"])),
                ("space_shooter_2", lambda s: space_shooter.ShooterGame(s, difficulty=2), "SS2.png", "Kepler-186f", "Kepler-186fSpec.png",
                 lambda s: qcm.QCMGame(s, questions=[
        ("How many terrestrial planets are estimated to exist in the Milky Way galaxy?", ["1 billion", "5 billion", "10 billion", "20 billion"]),
        ("What are super-Earths?", ["Terrestrial exoplanets larger than Earth", "Gas giants", "Planets with no solid surface", "Exoplanets smaller than Earth"]),
    ], correct_answers=["3", "1"])),
                ("space_shooter_2", lambda s: space_shooter.ShooterGame(s, difficulty=3), "SS3.png", "Proxima Centauri b", "ProximaSpec.png",
                 lambda s: qcm.QCMGame(s, questions=[
        ("How far away is the TRAPPIST-1 system from Earth?", ["10 light-years", "20 light-years", "30 light-years", "40 light-years"]),
        ("What unique feature do binary star systems provide for terrestrial planets?", ["Increased gravity", "Harmful radiation", "Reduced harmful radiation levels", "Smaller orbits"]),
        ("What is Kepler-11 b known for?", ["Being the largest terrestrial planet", "Orbiting its star very closely", "Having a solid surface", "Being part of a binary star system"]),
    ], correct_answers=["4", "3", "2"])),
            ],
            [
                ("ground_fighter_2", lambda s: ground_fighter.GroundFighterGame(s), "k2.png", "K2-131b", "k2Spec.png",
                 lambda s: qcm.QCMGame(s, questions=[
        ("What is the mass range of super-Earths compared to Earth?", ["Less than Earth's mass", "1 to 2 times the mass of Earth", "2 to 10 times the mass of Earth", "More than 10 times the mass of Earth"]),
    ], correct_answers=["3"])),
                ("ground_fighter_2", lambda s: ground_fighter.GroundFighterGame(s), "kepler.png", "Kepler-452b", "keplerSpec.png",
                 lambda s: qcm.QCMGame(s, questions=[
        ("What defines a super-Earth in terms of its mass?", ["Larger than Earth's but smaller than gas giants", "Smaller than Earth", "Equal to Earth's mass", "Larger than gas giants like Uranus and Neptune"]),
        ("What types of materials can super-Earths be composed of?", ["Only gas", "Only rock", "Gas, rock, or a combination of both", "Liquid metals"]),
    ], correct_answers=["1", "3"])),
                ("ground_fighter_2", lambda s: ground_fighter.GroundFighterGame(s), "LHS.png", "LHS 1140b", "LHSSpec.png",
                 lambda s: qcm.QCMGame(s, questions=[
        ("What makes super-Earths particularly interesting to scientists?", ["They are the most massive exoplanets known", "They offer a glimpse into the diversity of planetary systems beyond our own", "They have solid surfaces only", "They have atmospheres similar to Earth"]),
        ("How does the mass of super-Earths compare to ice giants like Uranus and Neptune?", ["Heavier than ice giants", "Lighter than ice giants", "The same mass as ice giants", "None of the above"]),
        ("In addition to their mass, what characteristic is commonly studied in super-Earths?", ["Their proximity to Earth", "Their composition and atmosphere", "Their orbital speed", "Their rotation period"]),
    ], correct_answers=["2", "2", "2"])),
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
            
            for col, (game_key, game_class, image_name, display_name, spec_name, qcm_class) in enumerate(game_column):
                x = 300 + col * button_spacing
                unlocked = self.unlocked_levels[game_key][col]
                unlocked_info = self.unlocked_levels[game_key+"_info"][col]
                unlocked_qcm = self.unlocked_levels[game_key+"_qcm"][col]
                buttons.append(ImageButton(x, y, image_name, scale=0.5, game_class=game_class, display_name=display_name, unlocked=unlocked, game_key=game_key))
                buttons.append(ImageButton(x + 75,  y+10, "choice.png", scale=0.5,
                                           game_class=qcm_class,
                                           game_key=game_key+"_qcm", display_name=display_name, unlocked=unlocked_qcm, size=(40,40)))
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
            progress = sum(self.unlocked_levels[game_key+"_done"]) / len(self.unlocked_levels[game_key+"_done"])
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

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("ExoExplorer")
    pygame.display.set_icon(pygame.image.load('./assets/menu/icon.png'))
    menu = Menu(screen)
    
    while True:
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
            unlocked_levels_qcm = menu.unlocked_levels[game_key+"_qcm"]
            no_unlock = True
            for i, unlocked in enumerate(unlocked_levels):
                if not unlocked:
                    no_unlock = False
                    # unlocked_levels[i] = True
                    # unlocked_levels_info[i] = True
                    unlocked_levels_qcm[i-1] = True
                    break
            if no_unlock:
                unlocked_levels_qcm[-1] = True
            menu.buttons = menu.create_buttons()  # Update buttons after unlocking
            text = font.render("You Win!", True, GREEN)
        elif result == "ok":
            # Unlock the next level if available
            game_key = menu.hovered_button.game_key[:-4]
            unlocked_levels = menu.unlocked_levels[game_key]
            unlocked_levels_info = menu.unlocked_levels[game_key+"_info"]
            unlocked_levels_done = menu.unlocked_levels[game_key+"_done"]
            no_unlock = True
            for i, unlocked in enumerate(unlocked_levels):
                if not unlocked:
                    no_unlock = False
                    unlocked_levels[i] = True
                    unlocked_levels_info[i] = True
                    unlocked_levels_done[i-1] = True
                    break
            if no_unlock:
                unlocked_levels_done[-1] = True
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
