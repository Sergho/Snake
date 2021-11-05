import pygame as pg
import sys
import numpy as np
import os
import apple
import snake
import AI

TILE = 20
WIDTH = 20
HEIGHT = 20
FPS = 30

block_field = np.zeros((WIDTH, HEIGHT))
food_field	= np.zeros((WIDTH, HEIGHT))

AI 	= AI.AI(pg.KEYUP, "query", 49, 4, 0.1)
Apple = apple.Apple(block_field, food_field)
Snake = snake.Snake((WIDTH // 2, HEIGHT // 2), AI, block_field, food_field, 3)

pg.init()
screen = pg.display.set_mode((WIDTH * TILE, HEIGHT * TILE))
clock = pg.time.Clock()

def spawn_blocks():
	for i in range(WIDTH):
		for j in range(HEIGHT):
			if i == 0 or j == 0 or i == WIDTH - 1 or j == HEIGHT - 1:
				block_field[i][j] = 2

def draw_food():
	for i in range(WIDTH):
		for j in range(HEIGHT):
			if food_field[i][j] == 1:
				pg.draw.rect(screen, pg.Color("yellow"),(i * TILE, j * TILE, TILE, TILE))

def draw_blocks():
	for i in range(WIDTH):
		for j in range(HEIGHT):
			if block_field[i][j] == 2:
				pg.draw.rect(screen, pg.Color("red"),(i * TILE, j * TILE, TILE, TILE))
			if block_field[i][j] == 1:
				pg.draw.rect(screen, pg.Color("green"),(i * TILE, j * TILE, TILE, TILE))

#setup
spawn_blocks()

#load weights to the neural network
if os.path.getsize("cache/blocks.npy") != 0:
	blocks = np.load("./cache/blocks.npy")
	food = np.load("./cache/food.npy")
	Snake.controller.load_weights(blocks, food)
Apple.spawn()
while True:
	events = pg.event.get()
	for _event in events:
		if _event.type == pg.QUIT:
			pg.quit()
			sys.exit()

	screen.fill(0)

	Snake.controller.set_inputs(Snake.get_view(block_field), Snake.get_view(food_field))
	# Snake.controller.set_inputs(Snake.get_view(block_field))
	Snake.update_delta(events)
	if not Snake.move():
		pg.quit()
		sys.exit()

	if Snake.eaten():
		Apple.spawn()
	draw_food()
	draw_blocks()

	clock.tick(FPS)
	pg.display.flip()