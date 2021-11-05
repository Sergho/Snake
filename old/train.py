import pygame, sys, snake, UserControl
from random import randrange
import numpy as np

TILE_SIZE       = 16
COLS            = 40
WIDTH = HEIGHT  = COLS * TILE_SIZE
FONT_FILE       = "freesansbold.ttf"
WHITE           = (255,255,255, 165)

pygame.init()
pygame.font.init()

GAME_FONT = pygame.font.Font(FONT_FILE, 24)

screen = pygame.display.set_mode((WIDTH + 150, HEIGHT))
snake = snake.Snake((3,7), ctrl_strategy=UserControl.UserControl())

field = np.zeros([COLS, COLS])
print(field)

FPS = 60

clock = pygame.time.Clock()

#apple
appX = randrange(0, WIDTH//TILE_SIZE, 1)
appY = randrange(0, HEIGHT//TILE_SIZE,1)

def draw_net():
    for y in range(COLS):
        for x in range(COLS):
            pygame.draw.rect(screen, (25,150,100), ((x*TILE_SIZE,y*TILE_SIZE),(TILE_SIZE, TILE_SIZE)), 1)

def render_text():
    score_status_string = f"Your score: {snake.length}".format()
    score_status_text = GAME_FONT.render(score_status_string, True, WHITE)
    screen.blit(score_status_text, (WIDTH-10,40))

def draw_apple():
    pygame.draw.rect(screen, pygame.Color("yellow"),(appX*TILE_SIZE, appY*TILE_SIZE, TILE_SIZE, TILE_SIZE))


while True:
    events = pygame.event.get()
    move = False
    for _event in events:
        if _event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif _event.type == pygame.KEYUP:
            move = True

    if move:
        snake.process_keys(events=events)
        screen.fill(0)
        draw_net()
        render_text()
        snake.move()
        snake.draw_self(screen, TILE_SIZE)
        draw_apple()

    if snake.get_head()[0] == appX and snake.get_head()[1] == appY:
        snake.eat_apple()
        appX = randrange(0, WIDTH//TILE_SIZE, 1)
        appY = randrange(0, HEIGHT//TILE_SIZE,1)


    #destroy condition
    if snake.get_head()[0] < 0 or snake.get_head()[0] >= COLS or snake.get_head()[1] < 0 or snake.get_head()[1] >= COLS:
        sys.exit()


    # clock.tick(FPS)
    pygame.display.flip()

print(f"Your score: {snake.length}".format())