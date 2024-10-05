import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 800
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Shoot 'em Up")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Load images
def load_image(name, width=WIDTH, height=HEIGHT):
    fullname = os.path.join('assets', name)
    image = pygame.image.load(fullname).convert_alpha()
    size = image.get_size()
    scale = width / size[0], height / size[1]
    size = (int(size[0] * scale[0]), int(size[1] * scale[1]))
    return pygame.transform.scale(image, size)

# Load background image
background = load_image('background.png')

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image('player.png', 75, 100)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def shoot(self):
        return Bullet(self.rect.centerx, self.rect.top)

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image('enemy.png', 50, 50)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(1, 3)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_image('bullet.png', 10, 15)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# Power up class
class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image('powerup.png', 30, 30)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(3, 5)
        
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

# Explosion class
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = [load_image(f'explosion{i}.png', 50, 50) for i in range(1, 8)]  # Assuming you have 5 explosion images
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
                
# Button class for menu
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

# Game functions
def show_menu():
    new_game_button = Button(WIDTH//2 - 100, HEIGHT//2 - 50, 200, 50, "New Game", GREEN, WHITE, 32)
    quit_button = Button(WIDTH//2 - 100, HEIGHT//2 + 50, 200, 50, "Quit", RED, WHITE, 32)

    while True:
        window.blit(background, (0, 0))
        new_game_button.draw(window)
        quit_button.draw(window)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if new_game_button.is_clicked(event.pos):
                    return "new_game"
                if quit_button.is_clicked(event.pos):
                    return "quit"

def game():
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    explosions = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18)

    def update_fps():
        fps = 'FPS: '+str(int(clock.get_fps()))
        fps_text = font.render(fps, 1, pygame.Color("coral"))
        return fps_text

    GAME_DURATION = 60 * 1000  # 60 seconds in milliseconds
    start_time = pygame.time.get_ticks()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = player.shoot()
                    all_sprites.add(bullet)
                    bullets.add(bullet)

        all_sprites.update()

        if random.randint(1, 60) == 1:
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)
        
        if random.randint(1, 1000) == 1:
            power = PowerUp()
            all_sprites.add(power)
            powerups.add(power)
            
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            explosion = Explosion(hit.rect.center[0], hit.rect.center[1])
            all_sprites.add(explosion)
            explosions.add(explosion)
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

        hits = pygame.sprite.spritecollide(player, enemies, False)
        if hits:
            return "game_over"

        hits = pygame.sprite.spritecollide(player, powerups, True)
        if hits:
            for enemy in enemies:
                enemy.kill()
            
        window.blit(background, (0, 0))
        all_sprites.draw(window)
        window.blit(update_fps(), (10,0))

        # Update and draw the progression bar
        BAR_SIZE = int(WIDTH * 0.8)
        PADDING = (WIDTH - BAR_SIZE) // 2
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time
        progress = min(elapsed_time / GAME_DURATION, 1.0)
        bar_width = int(BAR_SIZE * progress)
        pygame.draw.rect(window, YELLOW, (PADDING, 0, bar_width, 20))
        pygame.draw.rect(window, WHITE, (PADDING, 0, BAR_SIZE, 20), 2)

        if elapsed_time >= GAME_DURATION:
            return "win"

        pygame.display.flip()
        clock.tick(60)

def show_game_over(result):
    font = pygame.font.SysFont("Arial", 64)
    if result == "win":
        text = font.render("You Win!", True, GREEN)
    else:
        text = font.render("Game Over", True, RED)
    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
    window.blit(background, (0, 0))
    window.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)

# Main game loop
def main():
    while True:
        choice = show_menu()
        if choice == "quit":
            break
        elif choice == "new_game":
            result = game()
            if result == "quit":
                break
            show_game_over(result)

    pygame.quit()

if __name__ == "__main__":
    main()