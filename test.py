import pygame
import random
import numpy as np

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FONT = pygame.font.SysFont("Arial", 36)

# Quantum constants
H_BAR = 0.05  # Reduced Planck constant
INITIAL_STATE = np.array([[1], [0]])  # Initial state |0>

# Game variables
player_score = 0
player_lives = 3
game_over = False

# Create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quantum Breakout")

clock = pygame.time.Clock()


# Game objects
class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((100, 20))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 8

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed_x = random.choice([-5, 5])
        self.speed_y = -5
        self.quantum_state = INITIAL_STATE

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        # Ball collision with walls
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speed_x = -self.speed_x
        if self.rect.top < 0:
            self.speed_y = -self.speed_y
        # Ball collision with paddle
        if self.rect.colliderect(paddle.rect):
            self.speed_y = -self.speed_y
            self.apply_quantum_effect()
        # Ball collision with bricks
        brick_hit = pygame.sprite.spritecollideany(self, bricks)
        if brick_hit:
            self.speed_y = -self.speed_y
            bricks.remove(brick_hit)
            self.apply_quantum_effect()
            global player_score
            player_score += 10
            if not bricks:
                game_over_message("You Win!")
            pygame.display.update()

    def apply_quantum_effect(self):
        # Simulate quantum collapse
        if random.random() < 0.2:  # 20% chance of collapse
            self.quantum_state = np.array([[1], [0]])  # Reset to |0>


class Brick(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        self.image = pygame.Surface((80, 30))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# Create sprites
all_sprites = pygame.sprite.Group()
paddle = Paddle()
ball = Ball()
all_sprites.add(paddle, ball)

bricks = pygame.sprite.Group()
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
for row in range(3):
    for col in range(10):
        brick = Brick(random.choice(colors), col * 80, row * 30 + 50)
        bricks.add(brick)
        all_sprites.add(brick)


# Functions
def draw_text(text, color, x, y):
    text_surface = FONT.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)


def game_over_message(message):
    global game_over
    game_over = True
    screen.fill(BLACK)
    draw_text(message, WHITE, WIDTH // 2, HEIGHT // 2)
    pygame.display.flip()


# Game loop
running = True
while running:
    clock.tick(FPS)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        # Update
        all_sprites.update()

        # Render
        screen.fill(BLACK)
        all_sprites.draw(screen)
        draw_text(f"Score: {player_score}", WHITE, 70, 20)
        draw_text(f"Lives: {player_lives}", WHITE, WIDTH - 70, 20)

        if ball.rect.bottom > HEIGHT:
            player_lives -= 1
            if player_lives == 0:
                game_over_message("Game Over!")
            else:
                ball.rect.center = (WIDTH // 2, HEIGHT // 2)

        pygame.display.flip()

pygame.quit()
