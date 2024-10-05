import pygame
import random
import os

# Initialize Pygame
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

class AssetManager:
    @staticmethod
    def load_image(name, width, height):
        fullname = os.path.join('assets', name)
        image = pygame.image.load(fullname).convert_alpha()
        return pygame.transform.scale(image, (width, height))

class GameObject(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        pass

class Player(GameObject):
    def __init__(self, x, y):
        super().__init__(AssetManager.load_image('player.png', 75, 100), x, y)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def shoot(self):
        return Bullet(self.rect.centerx, self.rect.top)

class Enemy(GameObject):
    def __init__(self):
        super().__init__(AssetManager.load_image('enemy.png', 50, 50), 
                         random.randint(0, WIDTH - 50), 
                         random.randint(-100, -40))
        self.speed = random.randint(1, 3)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

class Bullet(GameObject):
    def __init__(self, x, y):
        super().__init__(AssetManager.load_image('bullet.png', 10, 15), x, y)
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Mini Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 18)
        self.background = AssetManager.load_image('background.png', WIDTH, HEIGHT)
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

class ShooterGame(Game):
    def __init__(self):
        super().__init__()
        self.player = Player(WIDTH // 2, HEIGHT - 110)
        self.all_sprites.add(self.player)
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.start_time = pygame.time.get_ticks()
        self.game_duration = 60 * 1000  # 60 seconds

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = self.player.shoot()
                    self.all_sprites.add(bullet)
                    self.bullets.add(bullet)
        return True

    def update(self):
        super().update()
        if random.randint(1, 60) == 1:
            enemy = Enemy()
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)

        hits = pygame.sprite.groupcollide(self.enemies, self.bullets, True, True)
        for hit in hits:
            enemy = Enemy()
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)

        hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        if hits:
            return "game_over"

        elapsed_time = pygame.time.get_ticks() - self.start_time
        if elapsed_time >= self.game_duration:
            return "win"

    def draw(self):
        super().draw()
        self.draw_progress_bar()

    def draw_progress_bar(self):
        BAR_SIZE = int(WIDTH * 0.8)
        PADDING = (WIDTH - BAR_SIZE) // 2
        elapsed_time = pygame.time.get_ticks() - self.start_time
        progress = min(elapsed_time / self.game_duration, 1.0)
        bar_width = int(BAR_SIZE * progress)
        pygame.draw.rect(self.screen, YELLOW, (PADDING, 0, bar_width, 20))
        pygame.draw.rect(self.screen, WHITE, (PADDING, 0, BAR_SIZE, 20), 2)

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

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.background = AssetManager.load_image('background.png', WIDTH, HEIGHT)
        self.font = pygame.font.SysFont("Arial", 32)
        self.games = [
            ("Shooter Game", ShooterGame),
            # Add more games here
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
        
        game = game_class()
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