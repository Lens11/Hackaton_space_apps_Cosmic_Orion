import pygame
import utils

class SimpleBackgroundGame(utils.Game):
    def __init__(self, screen, image):
        super().__init__()
        self.screen = screen
        self.background = utils.AssetManager.load_image(image, 'menu', self.screen.get_width(), self.screen.get_height())
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
        return self.running

    def update(self):
        pass

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

    def run(self):
        while self.running:
            if not self.handle_events():
                return "quit"
            self.update()
            self.draw()
            self.clock.tick(60)
        return "quit"