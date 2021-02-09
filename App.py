import sys, pygame
sys.path.append('./classes')
import cv2
import numpy
import math
from TelloDrone import TelloDrone
from DroneState import *


def start():
    stateMachine = StateMachine()

    pygame.init()
    size = width, height = 720, 600
    screen = pygame.display.set_mode((size))

    drone = TelloDrone()
    drone.changeVideoSize(720, 600)
    drone.connect()

    print(drone.query_battery())

    if (drone.query_battery() < 10):
        print('Error Battery Too Low...')
        raise Exception('Error Battery Too Low')

    while stateMachine.isNotExit():
        # check for pygame events
        eventList = pygame.event.get()
        try:
            stateMachine.run(drone, screen, eventList)
        except:
            print('-- TRACKING FAILED --')
            drone._spd = 0
            stateMachine.forceExit()
            drone.turnOff()
            raise
    drone.turnOff()



if __name__ == "__main__":
    start()