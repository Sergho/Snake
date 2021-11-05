import pygame as pg

class Keys:
	def __init__(self, event_type):
		self.event_type = event_type

	def get_delta(self, last, events):
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