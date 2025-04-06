import pygame
import random
import sys
import time

# Spustenie Pygame
pygame.init()

# Definuje sa velkost obrazovky
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Setup display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Uhni sa blokom!")

# Farby
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# Player settings
player_width = 50
player_height = 50
player_x = SCREEN_WIDTH // 2 - player_width // 2
player_y = SCREEN_HEIGHT - player_height - 10
player_speed = 5
invincible = False
invincible_timer = 0

# Block settings
block_width = 50
block_height = 50
block_speed = 5

# Font
font = pygame.font.SysFont('Arial', 30)
game_over_font = pygame.font.SysFont('Arial', 60)

# Sound Effects
collision_sound = pygame.mixer.Sound("drblyrobo.mp3")
score_sound = pygame.mixer.Sound("endo.mp3")
background_music = pygame.mixer.Sound("background_music.mp3")
background_music.set_volume(0.2)
score_sound.set_volume(0.5)
collision_sound.set_volume(0.4)

# Global variables for score and high score
global high_score
global score
score = 0
high_score = 0

# Function to draw the player
def draw_player(x, y):
    pygame.draw.rect(screen, WHITE, (x, y, player_width, player_height))

# Function to create a new red block
def create_red_block():
    block_x = random.randint(0, SCREEN_WIDTH - block_width)
    return [block_x, -block_height, "red"]

# Function to create a new yellow block
def create_yellow_block():
    block_x = random.randint(0, SCREEN_WIDTH - block_width)
    return [block_x, -block_height, "yellow"]

# Function to display the score
def display_score(score):
    score_text = font.render(f"Skóre: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

# Function to display the Game Over screen with restart button
def game_over(score, high_score):
    high_score  # Ensure that the high score is updated
    game_over_text = game_over_font.render("PREHRAL SI", True, RED)
    score_text = font.render(f"Skóre: {score}", True, WHITE)
    high_score_text = font.render(f"Max Skóre: {high_score}", True, WHITE)
    restart_text = font.render("Hrať Znova", True, WHITE)
    screen.fill(BLACK)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(high_score_text, (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, SCREEN_HEIGHT // 1.7))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 1.5))
    pygame.display.flip()

    # Wait for click to restart the game
    waiting_for_restart = True
    while waiting_for_restart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    waiting_for_restart = False
                    reset_game()  # Restart the game

# Function to reset the game
def reset_game():
    global score, player_x, player_y, block_speed, invincible, invincible_timer
    score = 0  # Reset the score
    block_speed = 5  # Reset block speed
    player_x = SCREEN_WIDTH // 2 - player_width // 2  # Reset player position
    player_y = SCREEN_HEIGHT - player_height - 10
    invincible = False  # Reset invincibility
    invincible_timer = 0
    game()  # Start the game again

# Main game loop
def game():
    global score, high_score  # Make sure to use the global score and high_score
    background_music.play()
    collision_sound.stop()
    global player_x, player_y, block_speed, invincible, invincible_timer
    blocks = []

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Key press detection
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
            player_x += player_speed

        # Update blocks
        if random.randint(1, 100) <= 2:  # Chance to spawn a new red block
            blocks.append(create_red_block())
        if random.randint(1, 100) <= 1:  # Chance to spawn a new yellow block
            blocks.append(create_yellow_block())

        for block in blocks[:]:
            block[1] += block_speed
            if block[1] > SCREEN_HEIGHT:
                blocks.remove(block)

            # Collision detection with red blocks
            if block[2] == "red" and block[0] < player_x + player_width and block[0] + block_width > player_x and block[1] < player_y + player_height and block[1] + block_height > player_y:
                if not invincible:
                    collision_sound.play()  # Play collision sound
                    background_music.stop()
                    score_sound.stop()
                    if score > high_score:
                        high_score = score
                    game_over(score, high_score)  # Show game over screen
                    return

            # Collision detection with yellow blocks
            if block[2] == "yellow" and block[0] < player_x + player_width and block[0] + block_width > player_x and block[1] < player_y + player_height and block[1] + block_height > player_y:
                blocks.remove(block)
                score += 10
                score_sound.stop()
                score_sound.play()  # Play score sound

        # Make invincible player last for 5 seconds
        if invincible and time.time() - invincible_timer > 5:
            invincible = False

        # Increase difficulty by speeding up blocks over time
        if score % 50 == 0 and block_speed < 10:
            block_speed += 0.1

        # Fill the screen with black
        screen.fill(BLACK)

        # Draw player and blocks
        draw_player(player_x, player_y)
        for block in blocks:
            if block[2] == "red":
                pygame.draw.rect(screen, RED, (block[0], block[1], block_width, block_height))
            elif block[2] == "yellow":
                pygame.draw.rect(screen, YELLOW, (block[0], block[1], block_width, block_height))

        # Display score
        display_score(score)

        # Update the screen
        pygame.display.flip()

        # Set the FPS
        clock.tick(FPS)

# Run the game
game()
