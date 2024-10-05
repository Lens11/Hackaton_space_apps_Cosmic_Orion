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
        super().__init__(utils.AssetManager.load_image('player.png','ground_fighter', 75, 100), x, y)
        self.speed = 5
        self.fireballs = pygame.sprite.Group()
        self.max_health = 100
        self.current_health = 100
        self.direction = 1

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.direction = -1
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
            self.direction = 1

    def shoot(self):
        fireball = Fireball(self.rect.centerx, self.rect.top, self.direction)
        self.fireballs.add(fireball)
        return fireball

    def draw_health_bar(self, surface):
        # Dessine la barre de vie du joueur
        bar_width = 150
        bar_height = 20
        health_ratio = self.current_health / self.max_health
        pygame.draw.rect(surface, RED, (10, 10, bar_width, bar_height))  # Barre rouge (fond)
        pygame.draw.rect(surface, GREEN, (10, 10, bar_width * health_ratio, bar_height))  # Barre verte (vie)

class Fireball(GameObject):
    def __init__(self, x, y):
        super().__init__(utils.AssetManager.load_image('projectile.png','ground_fighter', 20, 20), x, y)
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()

class Enemy(GameObject):
    def __init__(self):
        if random.choice([True, False]):
            x = -50
        else:
            x = WIDTH
        y = HEIGHT - 120
        super().__init__(utils.AssetManager.load_image('enemy.png','ground_fighter', 50, 100), x, y)
        self.speed_x = random.randint(3, 6) * (-1 if x == WIDTH else 1)
        self.max_health = 60
        self.current_health = 60

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()

    def draw_health_bar(self, surface):
        # Dessine la barre de vie de l'ennemi
        bar_width = 50
        bar_height = 5
        health_ratio = self.current_health / self.max_health
        pygame.draw.rect(surface, RED, (self.rect.x, self.rect.y - 10, bar_width, bar_height))  # Fond rouge
        pygame.draw.rect(surface, GREEN, (self.rect.x, self.rect.y - 10, bar_width * health_ratio, bar_height))  # Barre verte

class GroundFighterGame:
    def __init__(self, screen):
        self.screen = screen
        self.background = utils.AssetManager.load_image('background.jpg','ground_fighter', WIDTH, HEIGHT)
        self.player = Player(WIDTH // 2, HEIGHT - 110)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.enemies = pygame.sprite.Group()
        self.fireballs = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 18)
        self.game_duration = 60 * 1000  # 60 secondes
        self.start_time = pygame.time.get_ticks()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    fireball = self.player.shoot()
                    self.all_sprites.add(fireball)
                    self.fireballs.add(fireball)
        return True

    def update(self):
        self.all_sprites.update()

        # Générer des ennemis à des intervalles aléatoires
        if random.randint(1, 60) == 1:
            enemy = Enemy()
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)

        # Collision boule de feu - ennemi
        hits = pygame.sprite.groupcollide(self.enemies, self.fireballs, False, True)
        for enemy in hits:
            enemy.current_health -= 20  # Les ennemis perdent 20 points de vie par tir
            if enemy.current_health <= 0:
                enemy.kill()

        # Collision joueur - ennemi
        if pygame.sprite.spritecollide(self.player, self.enemies, False):
            self.player.current_health -= 20  # Le joueur perd 20 points de vie par collision
            if self.player.current_health <= 0:
                return "game_over"

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        # Dessin des sprites
        self.all_sprites.draw(self.screen)

        # Dessiner les barres de vie
        self.player.draw_health_bar(self.screen)
        for enemy in self.enemies:
            enemy.draw_health_bar(self.screen)

        # Dessiner la barre de progression du temps
        self.draw_progress_bar()

        pygame.display.flip()

    def draw_progress_bar(self):
        # Dessine une barre de progression du temps en haut de l'écran
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
