import pygame
import random
import os
import utils

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
        super().__init__(utils.AssetManager.load_image('player.png', 75, 100), x, y)
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
        super().__init__(utils.AssetManager.load_image('enemy.png', 50, 50), 
                         random.randint(0, WIDTH - 50), 
                         random.randint(-100, -40))
        self.speed = random.randint(1, 3)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

class Bullet(GameObject):
    def __init__(self, x, y):
        super().__init__(utils.AssetManager.load_image('bullet.png', 10, 15), x, y)
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()



class ShooterGame(utils.Game):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
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


