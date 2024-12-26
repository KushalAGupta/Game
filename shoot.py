import random
import pygame
import math

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Generate random colors
def get_random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# CLASSES
class Block(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        self.image = pygame.Surface([20, 15])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(RED)
        self.rect = self.image.get_rect()

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([4, 10])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y -= 3

# Functions
def show_welcome_screen():
    while True:
        screen.fill(WHITE)
        title_font = pygame.font.Font(None, 74)
        text_font = pygame.font.Font(None, 36)

        title_text = title_font.render("Welcome to the Game", True, RED)
        start_text = text_font.render("Click to Start", True, BLACK)

        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 100))
        screen.blit(start_text, (screen_width // 2 - start_text.get_width() // 2, 200))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return

def show_congrats_screen():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 74)
    congrats_text = font.render("Congratulations!", True, RED)
    screen.blit(congrats_text, (screen_width // 2 - congrats_text.get_width() // 2, 150))
    pygame.display.flip()
    pygame.time.wait(3000)

def create_pattern(level):
    blocks = pygame.sprite.Group()
    if level == 1:
        # Level 1: Simple Grid
        for row in range(4):
            for col in range(10):
                x = col * 60 + 10
                y = row * 40 + 10
                block = Block(BLUE, x, y)
                blocks.add(block)

    elif level == 2:
        # Level 2: Triangle
        for row in range(5):
            for col in range(row + 1):
                x = screen_width // 2 - row * 30 + col * 60
                y = row * 40 + 10
                block = Block(get_random_color(), x, y)
                blocks.add(block)

    elif level == 3:
        # Level 3: Circle Pattern
        center_x = screen_width // 2
        center_y = screen_height // 3
        radius = 100
        for i in range(20):  # 20 blocks forming a circle
            angle = math.radians(i * (360 / 20))  # Convert degrees to radians
            x = center_x + int(radius * math.cos(angle))
            y = center_y + int(radius * math.sin(angle))
            block = Block(get_random_color(), x, y)
            blocks.add(block)

    return blocks

# Initialize pygame
pygame.init()

# Set screen dimensions
screen_width = 700
screen_height = 400
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption("Block Shooting Game")

# Create sprite groups
all_sprite_list = pygame.sprite.Group()
block_list = pygame.sprite.Group()
bullet_list = pygame.sprite.Group()

# Create the player
player = Player()
player.rect.y = 370
all_sprite_list.add(player)

# Game variables
done = False
clock = pygame.time.Clock()
score = 0
level = 1
max_levels = 3

# Show welcome screen
show_welcome_screen()

# Generate the first pattern
block_list.add(create_pattern(level))
all_sprite_list.add(block_list)

# Main game loop
while not done:
    # Event processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Fire bullet
            bullet = Bullet()
            bullet.rect.x = player.rect.x + player.rect.width // 2 - bullet.rect.width // 2
            bullet.rect.y = player.rect.y
            all_sprite_list.add(bullet)
            bullet_list.add(bullet)

    # Update sprites
    all_sprite_list.update()

    # Check for collisions
    for bullet in bullet_list:
        block_hit_list = pygame.sprite.spritecollide(bullet, block_list, True)
        for block in block_hit_list:
            bullet_list.remove(bullet)
            all_sprite_list.remove(bullet)
            score += 1

        # Remove bullet if it goes off-screen
        if bullet.rect.y < -10:
            bullet_list.remove(bullet)
            all_sprite_list.remove(bullet)

    # Check if all blocks are cleared
    if len(block_list) == 0:
        if level < max_levels:
            level += 1
            block_list.add(create_pattern(level))
            all_sprite_list.add(block_list)
        else:
            show_congrats_screen()
            done = True

    # Drawing the frame
    screen.fill(WHITE)
    all_sprite_list.draw(screen)

    # Display the score and level
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, BLACK)
    level_text = font.render(f"Level: {level}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
