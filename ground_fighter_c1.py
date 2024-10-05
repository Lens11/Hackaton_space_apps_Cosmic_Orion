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
        super().__init__(utils.AssetManager.load_image('space-suit.png', 'ground_fighter', 40, 65), x, y)
        self.speed = 5
        self.fireballs = pygame.sprite.Group()
        self.max_health = 100
        self.current_health = 100
        self.direction = 1  # 1 pour droite, -1 pour gauche

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.direction = -1
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
            self.direction = 1

    def shoot(self):
        fireball = Fireball(self.rect.centerx, self.rect.centery, self.direction)
        self.fireballs.add(fireball)
        return fireball

    def draw_health_bar(self, surface):
        bar_width = 60
        bar_height = 10
        health_ratio = self.current_health / self.max_health
        bar_y = self.rect.top -20  # Positionner la barre au-dessus du joueur
        pygame.draw.rect(surface, RED, (self.rect.x, bar_y, bar_width, bar_height))
        pygame.draw.rect(surface, GREEN, (self.rect.x, bar_y, bar_width * health_ratio, bar_height))

class Fireball(GameObject):
    def __init__(self, x, y, direction):
        super().__init__(utils.AssetManager.load_image('projectile.png', 'ground_fighter', 20, 20), x, y)
        self.speed_x = 10 * direction
        self.direction = direction

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()

class Enemy(GameObject):
    def __init__(self, speed_multiplier=1):
        side = random.choice(['left', 'right'])
        if side == 'left':
            x = 0
            direction = 1
        else:
            x = WIDTH
            direction = -1
        y = HEIGHT - 140
        super().__init__(utils.AssetManager.load_image('monster.png', 'ground_fighter', 25, 50), x, y)
        self.speed_x = random.randint(1, 4) * direction * speed_multiplier
        self.max_health = 40
        self.current_health = 40

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()

    def draw_health_bar(self, surface):
        bar_width = 30
        bar_height = 4
        health_ratio = self.current_health / self.max_health
        pygame.draw.rect(surface, RED, (self.rect.x, self.rect.y - 10, bar_width, bar_height))
        pygame.draw.rect(surface, GREEN, (self.rect.x, self.rect.y - 10, bar_width * health_ratio, bar_height))

class GroundFighterGame:
    def __init__(self, screen, difficulty=1):
        self.difficulty = difficulty
        self.screen = screen
        self.background = utils.AssetManager.load_image('background.jpg', 'ground_fighter', WIDTH, HEIGHT)
        self.player = Player(WIDTH // 2, HEIGHT - 160)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.enemies = pygame.sprite.Group()
        self.fireballs = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 18)
        self.game_duration = max(30, 60 - (self.difficulty * 10)) * 1000  # Shorter game for higher difficulty
        self.start_time = pygame.time.get_ticks()
        self.last_enemy_spawn = 0
        self.enemy_spawn_delay = max(1500, 3000-(500*self.difficulty))  # 4 seconde entre chaque spawn d'ennemi

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

        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.start_time
        speed_multiplier_difficulty = (elapsed_time / self.game_duration)

        if current_time - self.last_enemy_spawn > self.enemy_spawn_delay:
            if self.difficulty == 1:
                num_enemies = random.choices([1, 2, 3], weights=[0.60, 0.27, 0.13])[0]
            elif self.difficulty == 2:
                num_enemies = random.choices([1, 2, 3], weights=[0.55, 0.29, 0.16])[0]
            else:
                num_enemies = random.choices([1, 2, 3], weights=[0.48, 0.31, 0.21])[0]
            for i in range(num_enemies):
                speed_multiplier = 0.15*self.difficulty + random.uniform(0.8, 1.3) * speed_multiplier_difficulty
                enemy = Enemy(speed_multiplier)
                self.all_sprites.add(enemy)
                self.enemies.add(enemy)
            self.last_enemy_spawn = current_time

        # Collision boule de feu - ennemi
        hits = pygame.sprite.groupcollide(self.enemies, self.fireballs, False, True)
        for enemy, fireballs in hits.items():
            enemy.current_health -= 20 * len(fireballs)  # 20 points de dégâts par boule de feu
            if enemy.current_health <= 0:
                enemy.kill()

        # Collision joueur - ennemi
        hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        for enemy in hits:
            self.player.current_health -= 20  # Le joueur perd 20 points de vie par collision
            enemy.kill()  # L'ennemi disparaît après avoir touché le joueur
            if self.player.current_health <= 0:
                return "game_over"

        # Vérifier si le temps est écoulé
        if pygame.time.get_ticks() - self.start_time >= self.game_duration:
            return "win"

        return None

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