import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quantum Breakout")

clock = pygame.time.Clock()

# Game variables
player_score = 0
player_lives = 3


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
        self.speed_x = 5
        self.speed_y = -5

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        # Ball collision with walls
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speed_x = -self.speed_x
        if self.rect.top < 0:
            self.speed_y = -self.speed_y
        # Ball collision with Paddle
        if self.rect.colliderect(paddle.rect):
            self.speed_y = -self.speed_y
        # Applying Quantum Quantum
        self.quantum_effects()

    def quantum_effects(self):
        if random.random() < 0.2:  # 20% chance of superposition
            self.rect.x += random.randint(-5, 5)
            self.rect.y += random.randint(-5, 5)

        # Entanglement
        if (
            self.rect.colliderect(paddle.rect) and random.random() < 0.1
        ):  # 10% chance of Entanglement
            self.speed_x = random.choice([-5, 5])
            self.speed_y = random.choice([-5, 5])

        # Uncertainy principle
        if random.random() < 0.1:  # 10% chance of Uncertainy
            self.speed_x += random.choice([-1, 1])
            self.speed_y += random.choice([-1, 1])


# Create sprites
all_sprites = pygame.sprite.Group()
paddle = Paddle()
ball = Ball()
all_sprites.add(paddle, ball)

# Game loop
running = True
while running:
    clock.tick(FPS)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    # Render
    screen.fill(BLACK)
    all_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()
