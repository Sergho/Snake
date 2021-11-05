from random import randrange

class Apple:

	def __init__(self, block_field, food_field):
		self.width = len(block_field)
		self.height = len(block_field[0])
		self.block_field = block_field
		self.food_field = food_field
		self.objects = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
		self.spawn()

	def get_field(self):
		return self.block_field[5][4];

	def get_size(self):
		return (self.width, self.height)

	def spawn(self):
		for i in range(len(self.objects)):
			print(self.objects[i])
			if self.block_field[self.objects[i][0]][self.objects[i][1]] != 0:
				print(1)
				self.food_field[self.objects[i][0]][self.objects[i][1]] = 0
				self.objects[i][0] = randrange(0, self.width, 1)
				self.objects[i][1] = randrange(0, self.height, 1)
				while self.block_field[self.objects[i][0]][self.objects[i][1]] != 0:
					self.objects[i][0] = randrange(0, self.width, 1)
					self.objects[i][1] = randrange(0, self.height, 1)
				self.food_field[self.objects[i][0]][self.objects[i][1]] = 1