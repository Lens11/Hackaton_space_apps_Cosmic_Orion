import pygame
import random
import utils

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
        super().__init__(utils.AssetManager.load_image('player.png', 30, 60), x, y)
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
        super().__init__(utils.AssetManager.load_image('enemy.png', 30, 30), 
        random.randint(0, WIDTH - 50), 
        random.randint(-100, -40))
        self.speed = random.randint(1, 3)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

class PowerUp(GameObject):
    def __init__(self):
        super().__init__(utils.AssetManager.load_image('powerup.png', 30, 30),
        random.randint(0, WIDTH - 30),
        random.randint(-100, -40))
        self.speed = random.randint(3, 5)
        
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

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = [utils.AssetManager.load_image(f'explosion{i}.png', 50, 50) for i in range(1, 8)]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50  # milliseconds

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.images):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.images[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class ShooterGame(utils.Game):
    def __init__(self, screen, difficulty=1):
        super().__init__()
        self.screen = screen
        self.player = Player(WIDTH // 2, HEIGHT - 110)
        self.all_sprites = pygame.sprite.Group(self.player)
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.start_time = pygame.time.get_ticks()
        self.background = utils.AssetManager.load_image('background.png', WIDTH, HEIGHT)
        self.game_duration = max(30, 60 - (difficulty * 10)) * 1000  # Shorter game for higher difficulty

        # Adjust game parameters based on difficulty
        self.enemy_spawn_rate = max(1, 48 - (difficulty * 10))  # More enemies at higher difficulty
        self.powerup_spawn_rate = max(500, 1000 - (difficulty * 50))  # More powerups at higher difficulty
        self.enemy_speed_range = (1 + difficulty, 3 + difficulty)  # Faster enemies at higher difficulty

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
        self.all_sprites.update()

        if random.randint(1, self.enemy_spawn_rate) == 1:
            enemy = self.create_enemy()
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)

        if random.randint(1, self.powerup_spawn_rate) == 1:
            powerup = PowerUp()
            self.all_sprites.add(powerup)
            self.powerups.add(powerup)

        hits = pygame.sprite.groupcollide(self.enemies, self.bullets, True, True)
        for hit in hits:
            explosion = Explosion(hit.rect.center[0], hit.rect.center[1])
            self.all_sprites.add(explosion)
            self.explosions.add(explosion)
            enemy = self.create_enemy()
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)

        hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        if hits:
            return "game_over"

        hits = pygame.sprite.spritecollide(self.player, self.powerups, True)
        if hits:
            for enemy in self.enemies:
                enemy.kill()

        elapsed_time = pygame.time.get_ticks() - self.start_time
        if elapsed_time >= self.game_duration:
            return "win"

    def create_enemy(self):
        enemy = Enemy()
        enemy.speed = random.randint(*self.enemy_speed_range)
        return enemy

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.all_sprites.draw(self.screen)
        self.draw_progress_bar()
        pygame.display.flip()

    def draw_progress_bar(self):
        BAR_SIZE = int(WIDTH * 0.8)
        PADDING = (WIDTH - BAR_SIZE) // 2
        elapsed_time = pygame.time.get_ticks() - self.start_time
        progress = min(elapsed_time / self.game_duration, 1.0)
        bar_width = int(BAR_SIZE * progress)
        t = bar_width / BAR_SIZE
        COLOR = (int(255*(1 - t)), int(255*t), 0)
        pygame.draw.rect(self.screen, COLOR, (PADDING, 0, bar_width, 20))
        pygame.draw.rect(self.screen, WHITE, (PADDING, 0, BAR_SIZE, 20), 2)

    def run(self):
        while True:
            if not self.handle_events():
                return "quit"
            result = self.update()
            if result:
                return result
            self.draw()
            self.clock.tick(FPS)