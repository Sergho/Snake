from pygame import *


class UserControl(object):
    """docstring for UserControl."""

    def __init__(self):
        print("User controller init!")

    def decide(self, events,cells=None, prev_pos=(0,0)):
        print(events)
        dx,dy = prev_pos
        for _event in events:
            if _event.type == KEYUP:
                if _event.key == K_w and dy !=  1:
                    dx, dy = 0,-1
                if _event.key == K_s and dy != -1:
                    dx, dy = 0, 1
                if _event.key == K_a and dx !=  1:
                    dx, dy =-1, 0
                if _event.key == K_d and dx != -1:
                    dx, dy = 1, 0
        return (dx,dy)