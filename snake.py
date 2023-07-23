import pygame
import numpy as np
import time
import random


# Initialize pygame
pygame.init()

# Define colors 
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
orange = (255, 165, 0)

# Define game display
width, height, tile_size = 600, 400, 10
game_display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake")
# Initialize game clock
clock = pygame.time.Clock()

# Define parameters for snake
snake_size = 10
snake_speed = 10
high_score = 0

# Define text fonts
message_font = pygame.font.SysFont("ubuntu", 30)
score_font = pygame.font.SysFont("ubuntu", 25)


def print_score(score):
    """
    Renders the score for the current round
    """
    text = score_font.render("Score: " + str(score), True, orange)
    game_display.blit(text, (0, 0))

def print_high_score(score):
    """
    Renders the highest score achieved for this instance
    """
    text = score_font.render("High Score: " + str(score), True, orange)
    game_display.blit(text, (width/2 - 50, 0))

def draw_snake(snake_size, snake_pixels):
    """
    Draws the pixels representing the snake
    """
    for pixel in snake_pixels:
        pygame.draw.rect(game_display, white, (pixel[0], pixel[1], snake_size, snake_size))


def run_game():
    # Game over parameter
    game_over = False
    # Exit game parameter
    game_close = False

    # Initial parameters
    x = width / 2
    y = height / 2
    x_speed = 0
    y_speed = 0
    snake_pixels = []
    snake_length = 1
    global high_score
    
    # Starting food position
    target_x = round(random.randrange(0, width - snake_size) / 10.0) * 10.0
    target_y = round(random.randrange(0, height - snake_size) / 10.0) * 10.0


    # Checkered background
    c = np.fromfunction(lambda x, y: (x//tile_size + y//tile_size) % 2, (width, height))
    checkered = np.full((width, height, 3), (128, 128, 128))
    checkered[c == 1] = (64, 64, 64)
    background = pygame.surfarray.make_surface(checkered)

    while not game_close:
        while game_over:
            # Game over screen
            game_display.fill(black)
            game_over_text = message_font.render("Game Over!", True, red)
            restart_text = score_font.render("Press [1] to restart", True, red)
            exit_text = score_font.render("Press [2] to exit", True, red)
            game_display.blit(game_over_text, (width/3, height/3))
            game_display.blit(restart_text, (width/3, height/2))
            game_display.blit(exit_text, (width/3, height/2 + 30))
            print_score(snake_length - 1)
            print_high_score(high_score)
            pygame.display.update()
            # Poll events
            for event in pygame.event.get():
                # Keydown events (K_1 = Restart game; K_2 = Exit game)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        run_game()
                    if event.key == pygame.K_2:
                        game_close = True
                        game_over = False
                # Quit game
                if event.type == pygame.QUIT:
                    game_close = True
                    game_over = False

        # Poll events
        for event in pygame.event.get():
            # Keydown events (Arrow left, Arrow right, Arrow up, Arrow down)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_speed == 0:
                    x_speed = -snake_speed
                    y_speed = 0
                    break
                if event.key == pygame.K_RIGHT and x_speed == 0:
                    x_speed = snake_speed
                    y_speed = 0
                    break
                if event.key == pygame.K_UP and y_speed == 0:
                    y_speed = -snake_speed
                    x_speed = 0
                    break
                if event.key == pygame.K_DOWN and y_speed == 0:
                    y_speed = snake_speed
                    x_speed = 0
                    break
            # Quit game
            if event.type == pygame.QUIT:
                game_close = True

        # If snake hits the screen bounds, then game is over
        if x >= width or x < 0 or y >= height or y < 0:
            game_over = True
        
        # Increment movement
        x += x_speed
        y += y_speed
        
        # Draw background
        game_display.blit(background, (0, 0))
        # Draw Food
        pygame.draw.rect(game_display, orange, [target_x, target_y, snake_size, snake_size])

        # Add pixel to head of snake and delete tail to simulate movement
        snake_pixels.append([x, y])
        if len(snake_pixels) > snake_length:
            del snake_pixels[0]

        # Self colissions (snake hits itself = game over)
        for pixel in snake_pixels[:-1]:
            if pixel == [x, y]:
                game_over = True
        
        draw_snake(snake_size, snake_pixels)
        print_score(snake_length - 1)
        if high_score < snake_length:
            high_score = snake_length - 1
        print_high_score(high_score)

        
        # If snake eats food, increase length and spawn new food
        if x == target_x and y == target_y:
            target_x = round(random.randrange(0, width - snake_size) / 10.0) * 10.0
            target_y = round(random.randrange(0, height - snake_size) / 10.0) * 10.0
            snake_length += 1
            print("Gobble Gobble Gob!")
        
        # Refresh game display
        pygame.display.update()
        # Set frame rate equal to snake speed
        clock.tick(snake_speed)
    
    pygame.quit()
    quit()




run_game()
