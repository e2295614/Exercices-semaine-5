import pygame
import random
import time
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT

def spawn_food():
    while True:
        gen_rnd = lambda x: random.randrange(1, (x//10))*10
        food = [gen_rnd(window_width), gen_rnd(window_height)]
        if food != snake_pos:
            return food

fps = 25

window_width = 720
window_height = 480

pygame.init()
pygame.display.set_caption("Snake Game")
game_window = pygame.display.set_mode((window_width, window_height))

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
KEYS = [K_UP, K_DOWN, K_RIGHT, K_LEFT]

fps_controller = pygame.time.Clock()

snake_pos = [100, 50]
snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]

food_pos = spawn_food()
food_spawn = True

direction = K_RIGHT
change_to = direction

score = 0

def show_score(color, font, size, game_over=0):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render(f"Score: {score}", True, color)
    score_rect = score_surface.get_rect()
    if not game_over:
        score_rect.midtop = (window_width/10, 15)
    else:
        score_rect.midtop = (window_width/2, window_height/1.25)
    game_window.blit(score_surface, score_rect)

def game_over():
    font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = font.render("Game Over", True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_width/2, window_height/4)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(green, 'times new roman', 30, 1)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    exit(0)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

        if event.type == pygame.KEYDOWN and event.key in KEYS:
            change_to = event.key

    if change_to == K_UP and direction != K_DOWN:
        direction = K_UP
    if change_to == K_DOWN and direction != K_UP:
        direction = K_DOWN
    if change_to == K_RIGHT and direction != K_LEFT:
        direction = K_RIGHT
    if change_to == K_LEFT and direction != K_RIGHT:
        direction = K_LEFT
    
    if direction == K_UP:
        snake_pos[1] -= 10
    if direction == K_DOWN:
        snake_pos[1] += 10
    if direction == K_RIGHT:
        snake_pos[0] += 10
    if direction == K_LEFT:
        snake_pos[0] -= 10

    snake_body.insert(0, list(snake_pos))
    if snake_pos == food_pos:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    if not food_spawn:
        food_pos = spawn_food()
        food_spawn = True

    game_window.fill(white)

    for pos in snake_body[1:]:
        pygame.draw.rect(game_window, red, [pos[0], pos[1], 10, 10])
    pygame.draw.rect(game_window, (150,0,0), [snake_body[0][0], snake_body[0][1], 10, 10])

    pygame.draw.rect(game_window, green, [food_pos[0], food_pos[1], 10, 10])

    if snake_pos[0] < 0 or snake_pos[0] > window_width-10:
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] > window_height-10:
        game_over()

    if snake_pos in snake_body[1:]:
        game_over()

    show_score(black, "consolas", 40)

    pygame.display.update()

    fps_controller.tick(fps)
