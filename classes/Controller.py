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
    def __init__(self):
        self._mov_vector = [0, 0, 0, 0]
        self._spd_vector = [60, 60, 60, 60]
        self._spd = 60
        self._switch = {
                pygame.K_w : (0, 1),    #forward
                pygame.K_s : (0, -1),   #backward
                pygame.K_a : (1, -1),   #left
                pygame.K_d : (1, 1),    #right
                pygame.K_q : (3, -1),   #turn_left
                pygame.K_e : (3, 1),    #turn_right
                pygame.K_SPACE : (2, 1),    #up
                pygame.K_LSHIFT : (2, -1)   #down
            }
    
    """
    Handles mapping a keydown to a 
    specific movement and direction
    using a dictionary and an array
    """
    def key_down(self, key):
        if key in self._switch:
            dir = self._switch[key]
            self._mov_vector[dir[0]] = dir[1]
    
    """
    Handles mapping a keyup to a
    direction to be reset using
    the same dictionary and array
    as in key_up
    """
    def key_up(self, key):
        if key in self._switch:
            dir = self._switch[key]
            self._mov_vector[dir[0]] = 0

    """
    Resets the controller such that
    every value is 0.
    """
    def reset(self):
        for i in range(len(self._mov_vector)):
            self._mov_vector[i] = 0
    
    """
    Getters and Setters for movement
    properties
    """

    @property
    def forward_backward(self):
        return self._mov_vector[0]

    @forward_backward.setter
    def forward_backward(self, dir):
        if dir > 1 or dir < -1:
            raise Exception("Error, direction can be of magnitude 1")
        self._mov_vector[0] = dir
    
    @property
    def left_right(self):
        return self._mov_vector[1]
    
    @left_right.setter
    def left_right(self, dir):
        if dir > 1 or dir < -1:
            raise Exception("Error, direction can be of magnitude 1")
        self._mov_vector[1] = dir
    
    @property
    def up_down(self):
        return self._mov_vector[2]

    @up_down.setter
    def up_down(self, dir):
        if dir > 1 or dir < -1:
            raise Exception("Error, direction can be of magnitude 1")
        self._mov_vector[2] = dir
    
    @property
    def yaw(self):
        return self._mov_vector[3]
    
    @yaw.setter
    def yaw(self, dir):
        if dir >= 1 or dir <= -1:
            raise Exception("Error, direction can be of magnitude 1")
        self._mov_vector[3] = dir

    @property
    def cspeed(self):
        return self._spd
    
    @cspeed.setter
    def cspeed(self, value):
        if value > 100 or value < 0:
            raise Exception("Error speed must be a value\
                            between 0 and 100")
        self._spd = value
    
    # speed vector getters /setters

    @property
    def forward_backward_speed(self):
        return self._spd_vector[0]

    @forward_backward_speed.setter
    def forward_backward_speed(self, value):
        if value > 100 or value < 0:
            raise Exception("Error speed must be a value\
                            between 0 and 100")
        self._spd_vector[0] = value
    
    @property
    def left_right_speed(self):
        return self._spd_vector[1]
    
    @left_right_speed.setter
    def left_right_speed(self, value):
        if value > 100 or value < 0:
            raise Exception("Error speed must be a value\
                            between 0 and 100")
        self._spd_vector[1] = value
    
    @property
    def up_down_speed(self):
        return self._spd_vector[2]

    @up_down_speed.setter
    def up_down_speed(self, value):
        if value > 100 or value < 0:
            raise Exception("Error speed must be a value\
                            between 0 and 100")
        self._spd_vector[2] = value
    
    @property
    def yaw_speed(self):
        return self._spd_vector[3]
    
    @yaw_speed.setter
    def yaw_speed(self, value):
        if value > 100 or value < 0:
            raise Exception("Error speed must be a value\
                            between 0 and 100")
        self._spd_vector[3] = value