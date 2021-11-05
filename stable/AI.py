import pygame as pg
import numpy
import math
import random
import scipy.special

class AI:
	def __init__(self, event_type, action_type, inputnodes, outputnodes, learningrate):
		self.event_type = event_type
		self.action_type = action_type;

		self.inodes = inputnodes
		self.onodes = outputnodes

		self.block_wio = numpy.random.normal(0.0, pow(self.inodes, -0.5), (self.onodes, self.inodes))
		self.food_wio = numpy.random.normal(0.0, pow(self.inodes, -0.5), (self.onodes, self.inodes))

		self.lr = learningrate

		self.activation_function = lambda x: scipy.special.expit(x)

	def load_weights(self, block, food):
		self.block_wio = block
		self.food_wio = food
		print("WEIGHTS LOADED")

	def set_inputs(self, block_field, food_field):
		blocks = []
		for i in block_field:
			for j in i:
				blocks.append(j)
		self.block_inputs = blocks
		food = []
		for i in food_field:
			for j in i:
				food.append(j)
		self.food_inputs = food

	def set_target(self, last, events):
		last_dx, last_dy = last
		for _event in events:
			if _event.type == self.event_type:
				if _event.key == pg.K_w and last_dy != 1:
					self.target = (1, 0, 0, 0)
				if _event.key == pg.K_s and last_dy != -1:
					self.target = (0, 1, 0, 0)
				if _event.key == pg.K_d and last_dx != -1:
					self.target = (0, 0, 0, 1)
				if _event.key == pg.K_a and last_dx != 1:
					self.target = (0, 0, 1, 0)

	def train(self):
		block_inputs_list = self.block_inputs
		food_inputs_list = self.food_inputs
		targets_list = self.target
		block_inputs = numpy.array(block_inputs_list, ndmin=2).T
		food_inputs = numpy.array(food_inputs_list, ndmin=2).T
		targets = numpy.array(targets_list, ndmin=2).T

		# for blocks
		block_outputs_inputs = numpy.dot(self.block_wio, block_inputs)
		block_final_outputs = self.activation_function(block_outputs_inputs)
		block_output_errors = targets - block_final_outputs
		self.block_wio += self.lr * numpy.dot((block_output_errors * block_final_outputs * (1.0 - block_final_outputs)), numpy.transpose(block_inputs))

		# for food
		food_outputs_inputs = numpy.dot(self.food_wio, food_inputs)
		food_final_outputs = self.activation_function(food_outputs_inputs)
		food_output_errors = targets - food_final_outputs
		self.food_wio += self.lr * numpy.dot((food_output_errors * food_final_outputs * (1.0 - food_final_outputs)), numpy.transpose(food_inputs))

	def sigmoid(self, x):
			return 1 / (1 + numpy.exp(-x))

	def MSE(self, y, Y):
		return numpy.mean((y - Y) ** 2)

	def get_delta(self, last, events):
		if self.action_type == "train":
			last_dx, last_dy = last
			for _event in events:
				if _event.type == self.event_type:
					if _event.key == pg.K_w and last_dy != 1:
						return (0, -1)
					if _event.key == pg.K_s and last_dy != -1:
						return (0, 1)
					if _event.key == pg.K_d and last_dx != -1:
						return (1, 0)
					if _event.key == pg.K_a and last_dx != 1:
						return (-1, 0)
			return last
		if self.action_type == "query":

			# for blocks
			block_inputs_list = self.block_inputs
			print(block_inputs_list)
			block_inputs = numpy.array(block_inputs_list, ndmin=2).T
			block_output_inputs = numpy.dot(self.block_wio, block_inputs)
			block_results = self.activation_function(block_output_inputs)

			# for food
			food_inputs_list = self.food_inputs
			food_inputs = numpy.array(food_inputs_list, ndmin=2).T
			food_output_inputs = numpy.dot(self.food_wio, food_inputs)
			food_results = self.activation_function(food_output_inputs)
			
			# summate food and blocks
			results = block_results
			for i in range(len(food_results)):
				results[i] += food_results[i]

			# print(block_results, food_results, "-----")
			print(results)

			maximum = max(results)
			maxs = [i for i,j in enumerate(results) if j==maximum]
			random_index = random.randint(0, len(maxs) - 1)
			index = maxs[random_index]
			if index == 0 and last != (0, 1):
				print("UP")
				return (0, -1)
			if index == 1 and last != (0, -1):
				print("DOWN")
				return (0, 1)
			if index == 3 and last != (-1, 0):
				print("RIGHT")
				return (1, 0)
			if index == 2 and last != (1, 0):
				print("LEFT")
				return (-1, 0)
			return last

			# maximum = max(results)
			# for i in range(len(results)):
			# 	if results[i] == maximum:
			# 		if i == 0 and last != (0, 1):
			# 			print("UP")
			# 			return (0, -1)
			# 		if i == 1 and last != (0, -1):
			# 			print("DOWN")
			# 			return (0, 1)
			# 		if i == 3 and last != (-1, 0):
			# 			print("RIGHT")
			# 			return (1, 0)
			# 		if i == 2 and last != (1, 0):
			# 			print("LEFT")
			# 			return (-1, 0)
			# return last