import pygame
import random
import utils

# Constants
WIDTH = 800
HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

class Player(utils.GameObject):
    def __init__(self, x, y):
        super().__init__(utils.AssetManager.load_image('space-suit.png', 'space_jumper', 80, 80), x, y)
        self.velocity = 0
        self.gravity = 0.5
        self.jump_strength = -10

    def update(self):
        self.velocity += self.gravity
        self.rect.y += self.velocity

        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity = 0
        elif self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0

    def jump(self):
        self.velocity = self.jump_strength

class Obstacle(utils.GameObject):
    def __init__(self, x, y, width, height):
        super().__init__(pygame.Surface((width, height)), x, y)
        self.image.fill(GREEN)
        self.speed = 3

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

class Enemy(utils.GameObject):
    def __init__(self, x):
        super().__init__(utils.AssetManager.load_image('monster.png', 'space_jumper', 50, 50), x, HEIGHT // 2)
        self.speed = 2
        self.direction = 1

    def update(self):
        self.rect.y = self.direction
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.kill()

class Asteroid(utils.GameObject):
    def __init__(self):
        size = random.randint(30, 50)
        super().__init__(utils.AssetManager.load_image('ufo.png', 'space_jumper', size, size), 0, 0)
        self.speed = random.uniform(2, 5)
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = HEIGHT if random.choice([True, False]) else -self.rect.height

    def update(self):
        
        if self.rect.right < 0 or self.rect.left > WIDTH or self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()

class SpaceJumperGame:
    def __init__(self, screen, difficulty=1):
        self.difficulty = difficulty
        self.screen = screen
        self.background = utils.AssetManager.load_image('background.jpg', 'space_jumper', WIDTH, HEIGHT)
        self.player = Player(50, HEIGHT // 2)
        self.all_sprites = pygame.sprite.Group(self.player)
        self.obstacles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 18)
        self.distance = 0
        self.total_distance = 5000 + (self.difficulty * 1000)
        self.last_obstacle = 0
        self.last_asteroid = 0
        self.obstacle_frequency = max(1500, 3000 + (self.difficulty * 500))
        self.asteroid_frequency = 5000  # Un astéroïde toutes les 5 secondes en moyenne

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()
        return True

    def update(self):
        self.all_sprites.update()
        self.distance += 3 + self.difficulty

        # Generate obstacles
        if pygame.time.get_ticks() - self.last_obstacle > self.obstacle_frequency:
            height = random.randint(100, 300)
            large = random.randint(20,50)
            obstacle = Obstacle(WIDTH-90, random.choice([0, HEIGHT - height]), 20 + large, height)
            self.obstacles.add(obstacle)
            self.all_sprites.add(obstacle)
            self.last_obstacle = pygame.time.get_ticks()

        # Generate enemy for difficulty 1
        if self.difficulty == 1 and self.distance >= self.total_distance * 0.5 and len(self.enemies) == 0:
            enemy = Enemy(WIDTH - 100)
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)

        # Generate asteroids
        if pygame.time.get_ticks() - self.last_asteroid > self.asteroid_frequency:
            asteroid = Asteroid()
            self.asteroids.add(asteroid)
            self.all_sprites.add(asteroid)
            self.last_asteroid = pygame.time.get_ticks()

        # Check collisions
        if pygame.sprite.spritecollide(self.player, self.obstacles, False) or \
           pygame.sprite.spritecollide(self.player, self.enemies, False) or \
           pygame.sprite.spritecollide(self.player, self.asteroids, False):
            return "game_over"

        # Check win condition
        if self.distance >= self.total_distance:
            return "win"

        return None

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.all_sprites.draw(self.screen)
        self.draw_progress_bar()
        pygame.display.flip()

    def draw_progress_bar(self):
        BAR_SIZE = int(WIDTH * 0.8)
        PADDING = (WIDTH - BAR_SIZE) // 2
        progress = min(self.distance / self.total_distance, 1.0)
        bar_width = int(BAR_SIZE * progress)
        pygame.draw.rect(self.screen, YELLOW, (PADDING, 10, bar_width, 20))
        pygame.draw.rect(self.screen, WHITE, (PADDING, 10, BAR_SIZE, 20), 2)

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