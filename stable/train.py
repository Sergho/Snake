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
FPS = 10

block_field = np.zeros((WIDTH, HEIGHT))
food_field	= np.zeros((WIDTH, HEIGHT))

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

def save_weights(blocks, food):
	print("SAVING WEIGHTS...")
	blocks = np.array([
		[0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, -10, 0, 0, 0,
		0, 0, 3, 0, 3, 0, 0,
  	0, 0, 0, -10, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, -10, 0, 0, 0,
		0, 0, 3, 0, 3, 0, 0,
  	0, 0, 0, -10, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 3, 0, 0, 0,
		0, 0, -10, 0, -10, 0, 0,
  	0, 0, 0, 3, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 3, 0, 0, 0,
		0, 0, -10, 0, -10, 0, 0,
  	0, 0, 0, 3, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0]])
	food = np.array([
		[0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0,
  	0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0,
  	0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0,
  	0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0,
  	0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0]])
	print(blocks)
	np.save("cache/blocks", blocks)
	np.save("cache/food", food)

#setup
spawn_blocks()

AI 	= AI.AI(pg.KEYUP, "train", 49, 4, 0.1)
Apple = apple.Apple(block_field, food_field)
Snake = snake.Snake((WIDTH // 2, HEIGHT // 2), AI, block_field, food_field, 3)

pg.init()
screen = pg.display.set_mode((WIDTH * TILE, HEIGHT * TILE))
clock = pg.time.Clock()


#load weights to the neural network
if os.path.getsize("cache/blocks.npy") != 0:
	blocks = np.load("cache/blocks.npy")
	food = np.load("cache/food.npy")
	Snake.controller.load_weights(blocks, food)

while True:
	events = pg.event.get()
	for _event in events:
		if _event.type == pg.QUIT:
			save_weights(Snake.controller.block_wio, Snake.controller.food_wio)
			pg.quit()
			sys.exit()
	move = False
	for _event in events:
		if _event.type == pg.KEYUP:
			if _event.key == pg.K_w or _event.key == pg.K_s or _event.key == pg.K_d or _event.key == pg.K_a:
				move = True
				break
	if move:
		screen.fill(0)

		Snake.controller.set_inputs(Snake.get_view(block_field), Snake.get_view(food_field))
		# Snake.controller.set_inputs(Snake.get_view(block_field))
		# print(food_field, block_field)
		Snake.controller.set_target((Snake.dx, Snake.dy), events)
		for a in range(5000):
			Snake.controller.train()
		# print("---")
		Snake.update_delta(events)
		if not Snake.move():
			save_weights(Snake.controller.block_wio, Snake.controller.food_wio)
			pg.quit()
			sys.exit()
		if Snake.eaten():
			Apple.spawn()
		

		draw_food()
		draw_blocks()
		move = False

	clock.tick(FPS)
	pg.display.flip()