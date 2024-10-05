import pygame
import utils

class SimpleBackgroundGame(utils.Game):
    def __init__(self, screen, image, menu):
        super().__init__()
        self.screen = screen
        self.background_image_name = image  # Store the image filename
        self.background = utils.AssetManager.load_image(image, 'menu', self.screen.get_width(), self.screen.get_height())
        self.running = True
        self.menu = menu  # Store reference to the menu
        
        # Create return button
        button_image = utils.AssetManager.load_image('back.png', 'menu', 40, 40)
        self.return_button = pygame.Rect(20, 20, 40, 40)
        self.return_button_image = button_image

        self.play_button_image = utils.AssetManager.load_image('PLAY.png', 'menu', 240, 80)
        button_y = self.screen.get_height() - 100  # Position the button 100 pixels from the bottom
        self.play_button = pygame.Rect(self.screen.get_width() // 2 - 120, button_y, 240, 80)  # Adjusted to match image size
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.return_button.collidepoint(event.pos):
                    return False
                elif self.play_button.collidepoint(event.pos):
                    self.unlock_first_minigame()
                    return False  # Exit the game loop
        return self.running

    def update(self):
        pass

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.return_button_image, self.return_button)
        self.screen.blit(self.play_button_image, self.play_button)
        pygame.display.flip()

    def run(self):
        while self.running:
            if not self.handle_events():
                return "menu"  # Return to menu
            self.update()
            self.draw()
            self.clock.tick(60)
        return "quit"

    def unlock_first_minigame(self):
        # Determine which row this game belongs to
        for row, (image, _) in self.menu.starting_images.items():
            if image == self.background_image_name:
                # Unlock the first minigame in the corresponding row
                game_key = self.menu.games[row][0][0]  # Get the game key of the first game in this row
                self.menu.unlocked_levels[game_key][0] = True
                self.menu.buttons = self.menu.create_buttons()  # Update buttons after unlocking
                break