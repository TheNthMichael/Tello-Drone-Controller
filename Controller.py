import pygame
"""
Controller Class
for the Tello Edu drone:
    The switch statement
    and mov_vector can be
    changed to support
    more controls.
"""
class Controller:
    _instance = None
    def __init__(self):
        if Controller._instance is None:
            self.mov_vector = [0,0,0,0]
            self.spd = 60
            self.switch = {
                    pygame.K_w : (0, 1),
                    pygame.K_s : (0, -1),
                    pygame.K_a : (1, -1),
                    pygame.K_d : (1, 1),
                    pygame.K_q : (3, -1),
                    pygame.K_e : (3, 1),
                    pygame.K_SPACE : (2, 1),
                    pygame.K_LSHIFT : (2, -1)
                }
        else:
            raise Exception("Error, only one instance of a Controller class allowed")
    
    """
    Handles mapping a keydown to a 
    specific movement and direction
    using a dictionary and an array
    """
    def key_down(self, key):
        if key in self.switch:
            dir = self.switch[key]
            self.mov_vector[dir[0]] = dir[1]
    
    """
    Handles mapping a keyup to a
    direction to be reset using
    the same dictionary and array
    as in key_up
    """
    def key_up(self, key):
        if key in self.switch:
            dir = self.switch[key]
            self.mov_vector[dir[0]] = 0

    """
    Resets the controller such that
    every value is 0.
    """
    def reset(self):
        for i in range(len(self.mov_vector)):
            mov_vector[i] = 0
    
    """
    Getters and Setters for movement
    properties
    """

    @property
    def forward_backward(self):
        return self.mov_vector[0]

    @forward_backward.setter
    def forward_backward(self, dir):
        if dir > 1 or dir < -1:
            raise Exception("Error, direction can be of magnitude 1")
        self.mov_vector[0] = dir
    
    @property
    def left_right(self):
        return self.mov_vector[1]
    
    @left_right.setter
    def left_right(self, dir):
        if dir > 1 or dir < -1:
            raise Exception("Error, direction can be of magnitude 1")
        self.mov_vector[1] = dir
    
    @property
    def up_down(self):
        return self.mov_vector[2]

    @up_down.setter
    def up_down(self, dir):
        if dir > 1 or dir < -1:
            raise Exception("Error, direction can be of magnitude 1")
        self.mov_vector[2] = dir
    
    @property
    def yaw(self):
        return self.mov_vector[3]
    
    @yaw.setter
    def yaw(self, dir):
        if dir > 1 or dir < -1:
            raise Exception("Error, direction can be of magnitude 1")
        self.mov_vector[3] = dir

    @property
    def speed(self):
        return self.spd
    
    @speed.setter
    def speed(self, value):
        if value > 100 or value < 0:
            raise Exception("Error speed must be a value\
                            between 0 and 100")
        self.spd = value
    
    