import numpy as np
class Snake:

	def __init__(self, position, controller, block_field, food_field, view_distance=3):
		self.x, self.y = position
		self.controller = controller
		self.block_field = block_field
		self.food_field = food_field
		self.body = [(self.x, self.y)]
		self.length = 2
		self.dx = 0
		self.dy = 0
		self.view_distance = view_distance
		block_field[self.x][self.y] = 1

	def move(self):
		if self.dx == self.dy:
			return True
		self.x += self.dx
		self.y += self.dy
		if self.block_field[self.x][self.y] == 2 or self.block_field[self.x][self.y] == 1:
			return False
		# Draw head
		self.body.append((self.x, self.y))
		self.block_field[self.x][self.y] = 1
		# Remove tail
		last = self.body[0]
		self.block_field[last[0]][last[1]] = 0
		self.body = self.body[-self.length:]
		return True

	def grow(self):
		self.length += 1

	def get_head(self):
		return self.body[-1]

	def update_delta(self, events):
		if self.controller != None:
			(self.dx, self.dy) = self.controller.get_delta((self.dx, self.dy), events)

	def get_view(self, field):
		dist = self.view_distance
		size = dist * 2 + 1
		result = np.zeros((size, size))
		for i in range(size):
			for j in range(size):
				field_i = self.x - dist + i
				field_j = self.y - dist + j
				if field_i >= 0 and field_j >= 0 and field_i < len(field) and field_j < len(field[0]):
					result[i][j] = field[field_i][field_j]
		return result


	def eaten(self):
		if self.food_field[self.x][self.y] == 1:
			self.grow()
			return True
		return False