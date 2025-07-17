import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 1000, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Soccer Goal Shoot Game")

# Load assets
background = pygame.image.load("assets/background.gif")
player_img = pygame.image.load("assets/player.png")
goalie_img = pygame.image.load("assets/goalie.png")
defender_img = pygame.image.load("assets/defender.png")
ball_imgs = [pygame.image.load(f"assets/ball{i}.png") for i in range(1, 5)]
ball_imgs = [pygame.transform.scale(img, (30, 30)) for img in ball_imgs]

GOALIE_TOP = 135
GOALIE_BOTTOM = 585
DEFENDER_TOP = 100
DEFENDER_BOTTOM = 650

# Game variables
FPS = 60
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 36)

# Difficulty variables
level = 1
score = 0
difficulty_increment = 3

# Classes
class Player:
    def __init__(self):
        self.image = player_img
        self.rect = self.image.get_rect(midleft=(50, HEIGHT // 2))
        self.speed = 5

    def move(self, keys):
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < 150:
            self.rect.x += self.speed

    def draw(self):
        screen.blit(self.image, self.rect)


class Ball:
    def __init__(self):
        self.images = ball_imgs
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(-100, -100))  # off-screen initially
        self.speed_x = 0
        self.is_kicked = False

    def kick(self, x, y):
        if not self.is_kicked:
            self.rect.center = (x + 60, y  + 125)
            self.speed_x = 15
            self.is_kicked = True

    def update(self):
        if self.is_kicked:
            self.rect.x += self.speed_x
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

            # Reset if ball goes off screen
            if self.rect.left > WIDTH:
                self.is_kicked = False
                self.rect.x = -100

    def draw(self):
        if self.is_kicked:
            screen.blit(self.image, self.rect)


class Goalie:
    def __init__(self):
        self.image = goalie_img
        self.rect = self.image.get_rect(midright=(WIDTH - 250, HEIGHT // 2))
        self.speed = 2

    def update(self):
        # Move up/down automatically
        self.rect.y += self.speed
        if self.rect.top < GOALIE_TOP:
            self.rect.top = GOALIE_TOP
            self.speed = abs(self.speed)  # go down
        elif self.rect.bottom > GOALIE_BOTTOM:
            self.rect.bottom = GOALIE_BOTTOM
            self.speed = -abs(self.speed)  # go up

    def draw(self):
        screen.blit(self.image, self.rect)


class Defender:
    def __init__(self):
        self.image = defender_img
        self.rect = self.image.get_rect(center=(WIDTH // 2, random.randint(50, HEIGHT - 50)))
        self.speed = random.choice([3, -3])

    def update(self):
        self.rect.y += self.speed
        if self.rect.top < DEFENDER_TOP:
            self.rect.top = DEFENDER_TOP
            self.speed = abs(self.speed)
        elif self.rect.bottom > DEFENDER_BOTTOM:
            self.rect.bottom = DEFENDER_BOTTOM
            self.speed = -abs(self.speed)

    def draw(self):
        screen.blit(self.image, self.rect)


# Initialize objects
player = Player()
ball = Ball()
goalie = Goalie()
defenders = []  # Start with no defenders

# Main game loop
running = True
while running:
    clock.tick(FPS)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ball.kick(player.rect.x, player.rect.y)

    # Update game objects
    player.move(keys)
    ball.update()
    goalie.update()
    for defender in defenders:
        defender.update()

    # Collision detection
    if ball.rect.colliderect(goalie.rect):
        ball.is_kicked = False
        ball.rect.x = -100
    for defender in defenders:
        if ball.rect.colliderect(defender.rect):
            ball.is_kicked = False
            ball.rect.x = -100

    # Goal detection
    if ball.rect.right >= WIDTH:
        score += 1
        ball.is_kicked = False
        ball.rect.x = -100

        # Increase difficulty every 3 goals
        if score % difficulty_increment == 0:
            level += 1
            goalie.speed += 1  # make goalie faster
            # Spawn defenders starting at level 3
            if level >= 3 and len(defenders) < 1:
                defenders.append(Defender())
            elif level >= 4 and len(defenders) < 2:
                defenders.append(Defender())
            # Speed up defenders
            for defender in defenders:
                defender.speed += 1 if defender.speed > 0 else -1

    # Draw everything
    screen.blit(background, (0, 0))
    player.draw()
    goalie.draw()
    for defender in defenders:
        defender.draw()
    ball.draw()

    # Display score and level
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    level_text = font.render(f"Level: {level}", True, (255, 255, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 50))

    pygame.display.flip()
