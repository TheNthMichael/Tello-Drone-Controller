import sys, pygame
sys.path.append('./classes')
import cv2
import numpy
import math
from TelloDrone import TelloDrone
from Controller import Controller
from DroneState
from Face import Face
from Pid import Pid

if __name__ == "__main__":
    start()

def start():
    drone = TelloDrone()
    drone.changeVideoSettings(720, 600)

    state = DroneState.Waiting()

    pygame.init()
    size = width, height = 720, 600
    screen = pygame.display.set_mode((size))
    img = pygame.Surface((width, height))

    print(drone.query_battery())

    while state.state_type != DroneState.States.EXIT:
        # check for pygame events
        eventList = pygame.event.get()
        try:
            tmp_state = state.action(drone, eventList)
            if tmp_state != None:
                state.clean()
                state = tmp_state
        except:
            print('-- TRACKING FAILED --')
            state.clean()
            state = state.change(DroneState.States.EXIT)
            raise
    drone.turnOff()
    cv2.destroyAllWindows()